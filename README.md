# Quotation-Detection-on-RiQuA-Dataset
Quotation detection is an important processing step in a variety of applications in machine learning, including generative applications like audiobook or script generation and classification applications such as automated fact checking.

RiQuA, Rich Quotation Annotations is a corpus that provides quotations for English literary text. RiQuA dataset consists of 15 excerpts from 11 works of 19th century English novels by 6 authors. Some of the works include Jane Austen’s ”Emma”, Anton Chekhov’s ”The Lady with the Dog” and Mark Twain’s ”The Adventures of Tom Sawyer”.

Quotation detection can be challenging since most words are not significantly more likely to be inside or outside of a quotation, so a quotation detection model needs to have some understanding of the context surrounding words. In this project, we experiment with various models for quotation detection, focusing on methods that do not require excessive feature engineering. We evaluate a simple most common tag baseline, a number of supervised models trained on BERT embeddings, and a fine-tuned BERT model, and we find that BERT is able to embed the context around each token to significantly improve performance over the baseline.

|<img width="578" alt="image" src="https://user-images.githubusercontent.com/68454938/211204928-61823203-d652-48d9-9397-6f275073943d.png">
|:--:| 
| *Example 1* |

|![image](https://user-images.githubusercontent.com/68454938/211204946-c95f86f6-9ae2-43ef-ba64-101826902e85.png)
|:--:| 
| *Example 2* |

|<img width="565" alt="q3-1" src="https://user-images.githubusercontent.com/68454938/211205044-1d2b815e-8e02-4c2f-865b-707255578d09.png">
|:--:| 
| *Example 3* |


|<img width="714" alt="image" src="https://user-images.githubusercontent.com/68454938/211205111-036ef8c4-34e6-4461-8f44-4dda09cd3765.png">
|:--:| 
| *Word Embeddings* |

We found that, as expected, the most common tag has some success in identifying cue words but fails spectacularly at identifying quotations, and the BERT-based models that are able to capture more context perform better. The fine-tuned model performs the best, with an F1 score of 0.75 both on quotations and overall, falling a bit short of the state-of-the-art of around 0.85. KNN and Naive Bayes both significantly outperformed the most common tag baseline but still fell far short of the finetuned model, achieving F1 scores of 0.20 and 0.23 on quotations in the test set, respectively. The Logistic Regression model, however, was able to approach the performance of the finetuned model, reaching 0.65 F1 on quotations in the test set.

|![image](https://user-images.githubusercontent.com/68454938/211205087-d558dd83-1568-437b-9e09-675162c61e05.png)
|:--:| 
| *Cue word cloud* |

|![image](https://user-images.githubusercontent.com/68454938/211205099-6946e8da-f2c2-4d53-864d-9469e90349a6.png)
|:--:| 
| *Entity word cloud* |

<img width="954" alt="image" src="https://user-images.githubusercontent.com/68454938/224436909-c2f99a44-98e4-4cdd-9a1a-33bc2c4dfced.png">

# References

[1] Tom B. Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, Sandhini Agarwal, Ariel Herbert-Voss, Gretchen Krueger, Tom Henighan, Rewon Child, Aditya Ramesh, Daniel M. Ziegler, Jeffrey Wu, Clemens Winter, Christopher Hesse, Mark Chen, Eric Sigler, Mateusz Litwin, Scott Gray, Benjamin Chess, Jack Clark, Christopher Berner, Sam McCandlish, Alec Radford, Ilya Sutskever, and Dario Amodei. Language models are few-shot learners, 2020. 

[2] Yue Chen, Zhen-Hua Ling, and Qing-Feng Liu. A Neural-Network-Based Approach to Identifying Speak- ers in Novels. In Interspeech 2021, pages 4114–4118. ISCA, August 2021.

