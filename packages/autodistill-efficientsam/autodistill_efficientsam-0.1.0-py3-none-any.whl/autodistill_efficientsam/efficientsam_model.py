import os
from dataclasses import dataclass

import torch

import supervision as sv
from autodistill.detection import CaptionOntology, DetectionBaseModel
from autodistill.helpers import load_image

HOME = os.path.expanduser("~")
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

import torch
import numpy as np
from torchvision.transforms import ToTensor

GPU_EFFICIENT_SAM_CHECKPOINT = "efficient_sam_s_gpu.jit"
CPU_EFFICIENT_SAM_CHECKPOINT = "efficient_sam_s_cpu.jit"


def load(device: torch.device) -> torch.jit.ScriptModule:
    if device.type == "cuda":
        model = torch.jit.load(HOME + "/.autodistill/" + GPU_EFFICIENT_SAM_CHECKPOINT)
    else:
        model = torch.jit.load(HOME + "/.autodistill/" + CPU_EFFICIENT_SAM_CHECKPOINT)
    model.eval()
    return model


def inference_with_box(
    image: np.ndarray,
    box: np.ndarray,
    model: torch.jit.ScriptModule,
    device: torch.device,
) -> np.ndarray:
    bbox = torch.reshape(torch.tensor(box), [1, 1, 2, 2])
    bbox_labels = torch.reshape(torch.tensor([2, 3]), [1, 1, 2])
    img_tensor = ToTensor()(image)

    predicted_logits, predicted_iou = model(
        img_tensor[None, ...].to(device),
        bbox.to(device),
        bbox_labels.to(device),
    )
    predicted_logits = predicted_logits.cpu()
    all_masks = torch.ge(torch.sigmoid(predicted_logits[0, 0, :, :, :]), 0.5).numpy()
    predicted_iou = predicted_iou[0, 0, ...].cpu().detach().numpy()

    max_predicted_iou = -1
    selected_mask_using_predicted_iou = None
    for m in range(all_masks.shape[0]):
        curr_predicted_iou = predicted_iou[m]
        if (
            curr_predicted_iou > max_predicted_iou
            or selected_mask_using_predicted_iou is None
        ):
            max_predicted_iou = curr_predicted_iou
            selected_mask_using_predicted_iou = all_masks[m]
    return selected_mask_using_predicted_iou


@dataclass
class EfficientSAM(DetectionBaseModel):
    ontology: CaptionOntology

    def __init__(self, ontology: CaptionOntology):
        # if ~/.autodistill/efficient_sam_s_gpu.jit does not exist, download it
        # media.roboflow.com/efficient_sam_s_cpu.jit
        if (
            not os.path.exists(HOME + "/.autodistill/" + GPU_EFFICIENT_SAM_CHECKPOINT)
            and DEVICE.type == "cuda"
        ):
            os.system(
                f"wget -O {HOME}/.autodistill/{GPU_EFFICIENT_SAM_CHECKPOINT} https://media.roboflow.com/{GPU_EFFICIENT_SAM_CHECKPOINT}"
            )
        if (
            not os.path.exists(HOME + "/.autodistill/" + CPU_EFFICIENT_SAM_CHECKPOINT)
            and DEVICE.type == "cpu"
        ):
            os.system(
                f"wget -O {HOME}/.autodistill/{CPU_EFFICIENT_SAM_CHECKPOINT} https://media.roboflow.com/{CPU_EFFICIENT_SAM_CHECKPOINT}"
            )

        self.model = load(device=DEVICE)

    def predict(self, input: str, confidence: int = 0.5) -> sv.Detections:
        image = load_image(input)
        height, width, _ = image.shape
        box = np.array([[0, 0], [width, height]])

        results = inference_with_box(image, box, self.model, DEVICE)
        # reshape to (N, W, H) from (W, H)
        xyxys = sv.mask_to_xyxy(np.array([results]))

        detections = sv.Detections(
            xyxy=np.array(xyxys),
            mask=np.array([results]),
            confidence=np.array([1.0] * len(xyxys)),
            class_id=np.array([0] * len(xyxys)),
        )

        detections = detections[detections.confidence > confidence]

        return detections
