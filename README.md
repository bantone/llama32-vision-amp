# Image Analysis with Anthropic's Claude LLM
This Accelerator for Machine Learning Projects ("AMP") allows users to perform transcription and information extraction on images using Meta's Llama 3.2 Vision model.  This model is ideal for applications requiring sophisticated visual intelligence, such as image analysis, document processing, multimodal chatbots, and autonomous systems.
 
![](/assets/llama-meta-logo.png)


## Use Cases Solved With Llama 3.2 Vision Models

1. **Visual Question Answering (VQA) and Visual Reasoning**: Imagine a machine that looks at a picture and understands your questions about it.

2. **Document Visual Question Answering (DocVQA)**: Imagine a computer understanding both the text and layout of a document, like a map or contract, and then answering questions about it directly from the image.

3. **Image Captioning**: Image captioning bridges the gap between vision and language, extracting details, understanding the scene, and then crafting a sentence or two that tells the story.

4. **Image-Text Retrieval**: Image-text retrieval is like a matchmaker for images and their descriptions. Similar to a search engine but one that understands both pictures and words.

5. **Visual Grounding**: Visual grounding is like connecting the dots between what we see and say. It’s about understanding how language references specific parts of an image, allowing AI models to pinpoint objects or regions based on natural language descriptions.


## Llama 3.2 90b - Cutting edge visual LLM

```
meta/llama-3.2-11b-vision-instruct
meta/llama-3.2-90b-vision-instruct
```
![](/assets/screenshots/claude-models.png)

**Llama 3.2 11B/90B:** The Llama 3.2-Vision collection of multimodal large language models (LLMs) is a collection of instruction-tuned image reasoning generative models in 11B and 90B sizes (text + images in / text out). The Llama 3.2-Vision instruction-tuned models are optimized for visual recognition, image reasoning, captioning, and answering general questions about an image. The models outperform many of the available open source and closed multimodal models on common industry benchmarks.

## Using the Application

### 1. Transcribing Typed Text
The app can easily extract clean and accurate text from typed or printed images, such as scanned PDFs or printouts, allowing users to quickly digitize documents.

![](/assets/screenshots/transcribing-typed-text.png)

### 2. Transcribing Handwritten Text
With powerful recognition capabilities, the app can process handwritten notes from images, making it possible to convert personal writings into editable, searchable digital formats.

![](/assets/screenshots/transcribing-handwritten-text.png)

### 3. Transcibing Forms
The app preserves the structure and layout of forms while extracting content, ensuring that complex tables, questionnaires, and other structured documents are accurately digitized for data processing.

![](/assets/screenshots/transcribing-forms.png)

### 4. Complicated Document QA
Users can ask specific questions about the content of a complex document, and the app leverages the Claude model's capabilities to understand and extract context-based answers from the image.

![](/assets/screenshots/complicated-doc-qa.png)

### 5. Unstructured Information to JSONs
The app provides the functionality to convert unstructured or free-form content from images into structured JSON data, enabling easier integration with other systems or databases.

![](/assets/screenshots/unstructured-info-to-json.png)

### 6. User Defined Prompts
This feature allows users to input their own custom prompts for Claude to process the image in any way they need, offering advanced flexibility for various unique use cases not covered by predefined options.

![](/assets/screenshots/user-defined.png)

### 7. Upload Photos
Users can easily upload images for processing, manage their image library, and view or delete existing images, enabling efficient preparation for all use cases.

![](/assets/screenshots/upload-images.png)


## Deployment

### AMP Deployment Methods
There are two ways to launch this prototype on CML:

1. **From Prototype Catalog** - Navigate to the Prototype Catalog on a CML workspace, select the "Document Summarization with Gemini from Vertex AI" tile, click "Launch as Project", click "Configure Project".

2. **As ML Prototype** - In a CML workspace, click "New Project", add a Project Name, select "ML Prototype" as the Initial Setup option, copy in the [repo URL](https://github.com/bantone/llama32-vision-amp), click "Create Project", click "Configure Project".

### AMP Deployment
In both cases, you will need to specify the `NVIDIA_API_KEY` *(steps in next section on how to create this)* which enables the connection between Anthropic's API and the Application in CML.

![](/assets/screenshots/amp-setup.png)

![](/assets/screenshots/amp-build-script.png)

## Requirements

### Setup NVIDIA API Key

Navigate to https://build.nvidia.com/ and sign up for an account.

![](/assets/screenshots/nvidia-setup-1.png)

![](/assets/screenshots/nvidia-setup-2.png)

![](/assets/screenshots/nvidia-setup-3.png)


#### Recommended Runtime
JupyterLab - Python 3.11 - Standard - 2024.05

#### Resource Requirements
This AMP creates the following workloads with resource requirements:
- CML Session: `2 CPU, 8GB MEM`
- CML Application: `2 CPU, 8GB MEM`

#### External Resources
This AMP requires pip packages and models from huggingface. Depending on your CML networking setup, you may need to whitelist some domains:
- pypi.python.org
- pypi.org
- pythonhosted.org
- huggingface.co

Additionally, it will require access to Anthropic's Claude API. Please ensure access to Claude is whitelisted as well.

## Deploying on CML
There are two ways to launch this prototype on CML:

1. **From Prototype Catalog** - Navigate to the Prototype Catalog on a CML workspace, select the "Intelligent QA Chatbot with NiFi, Pinecone, and Llama2" tile, click "Launch as Project", click "Configure Project"

2. **As ML Prototype** - In a CML workspace, click "New Project", add a Project Name, select "ML Prototype" as the Initial Setup option, copy in the [repo URL](https://github.com/cloudera/CML_AMP_Image-Analysis-with-Anthropic-Claude), click "Create Project", click "Configure Project"


## The Fine Print

IMPORTANT: Please read the following before proceeding.  This AMP includes or otherwise depends on certain third party software packages.  Information about such third party software packages are made available in the notice file associated with this AMP.  By configuring and launching this AMP, you will cause such third party software packages to be downloaded and installed into your environment, in some instances, from third parties' websites.  For each third party software package, please see the notice file and the applicable websites for more information, including the applicable license terms.

If you do not wish to download and install the third party software packages, do not configure, launch or otherwise use this AMP.  By configuring, launching or otherwise using the AMP, you acknowledge the foregoing statement and agree that Cloudera is not responsible or liable in any way for the third party software packages.


Refer to the Project **NOTICE** and **LICENSE** files in the root directory. Author: Cloudera Inc.
