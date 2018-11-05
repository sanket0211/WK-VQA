## Abstract

Visual Question Answering (VQA) has emerged as an important Computer Vision task. In conventional VQA, one may ask questions about an image which can be answered purely based on its content. For example, given an image with people in it, a typical VQA question may inquire about the number of people in the image. More recently, there is growing interest in answering questions which require commonsense knowledge involving common nouns (e.g., cats, dogs, microphones.) present in the image. In spite of this progress, the important problem of answering questions requiring world knowledge about named entities (e.g., Barack Obama, White House.) in the image has not been addressed in prior research. We address this gap in this paper, and introduce WK-VQA – the first dataset for the task of World Knowledge-enabled VQA. WK-VQA consists of 193K question-answer pairs involving more than 19K named entities and 25K images. Questions in this dataset require multi-entity, multi-relation, and multi-hop reasoning over large Knowledge Graphs (KG) to arrive at an answer. To the best of our knowledge, WKVQA is the largest dataset for exploring VQA over KG. Further, we also provide baseline performances using state-ofthe-art methods for world knowledge-enabled VQA on WKVQA. We firmly believe that WK-VQA will spawn new avenues of research spanning the areas of vision, language, knowledge graphs, and more broadly AI.

### CODE

Github Repository of code [repo link](#)

### PAPER

Please download the paper here [paper link](#)

### AAAI 2019 SLIDES

Please download the slides here [slides link](#)

### BIBTEX

### DATASET

Please [click here](#) to download the dataset WK-VQA


```markdown
The following files and folders can be found in the dataset

1. WK-VQA-1.0
- Folder 1: WK-VQA_images
- Folder 2: WK-VQA_reference_images
- File 1: dataset.json which contains the following
{
	ImgId:{
		'NamedEntities': A list of named entities present in the image, 
		'Qids': Corresponding of Qids,
		'wikiCap': Wiki Caption associated with the image,
		'Questions': A list of questions associated with the image,
		'Answers': A list of answers to the questions,
		'ParaQuestions': Paraphrase version of the questions,
		'Type of Question': A list of tags like Boolean, Spatial, etc for each question,
		'sourcePath': URL from where the image has been downloaded
	}
}


[Link](url) and ![Image](src)
```

