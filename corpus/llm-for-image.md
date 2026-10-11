# Multimodal LLMs & Vision

## Vision-language models (VLMs)

VLMs take image (+ optionally audio/video) **and text** and produce text.
Examples: CLIP (contrastive embeddings), LLaVA, GPT-4V/GPT-4o, Qwen-VL.
Typical design: a vision encoder produces image features, a connector maps
them into the LLM's embedding space, and the LLM decodes text.

## CLIP & contrastive learning

CLIP trains an image encoder and a text encoder so paired image/text
embeddings are pulled together and unpaired pairs are pushed apart
(contrastive loss). It enables **zero-shot classification**: embed candidate
labels as text, pick the most similar to the image. The same contrastive
recipe powers image-caption retrieval and multimodal search.

## Vision encoders

- **ViT** (Vision Transformer): an image is split into fixed-size **patches**
  (e.g., 16×16), each patch linearly projected into an embedding with a
  positional encoding — vision through the Transformer lens.
- **CNN backbones** (ResNet, ConvNeXt): still common for feature extraction.
- Object detection/segmentation heads (DETR, YOLO, SAM) can plug into the
  vision side of multimodal pipelines.

## Tasks

- **Image captioning / VQA**: answer questions about an image.
- **Document AI / OCR**: read text from scans (read order matters; models
  attend to the rendering of text).
- **Grounding**: refer to objects by location (boxes/masks).
- **Image-to-text for accessibility, search, and data extraction.**

## Image generation

- **Diffusion models**: iteratively denoise random noise to an image,
  conditioned on text (text-to-image). **Latent diffusion** operates in a
  compressed latent space (e.g., Stable Diffusion).
- **VAEs / GANs**: earlier generation approaches; GANs pit generator vs
  discriminator.
- Common content: control (pose/layout), inpainting, and **image editing**
  via text instructions.

## Failure modes & quality

- VLMs can **hallucinate** objects/details not in the image.
- OCR errors cascade into downstream text understanding.
- Measure with **human evaluation**, exact-match for structured outputs, and
  specialized benchmarks (e.g., DocVQA, MMMU, GQA).
- Watch for **bias in training data** (faces, skin tone, culture) — audit
  before deployment.