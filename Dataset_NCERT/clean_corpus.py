# -*- coding: utf-8 -*-

import re

string = """1. Discuss some of the social changes in nineteenth-century Britain which Thomas Hardy
and Charles Dickens wrote about.

3. In what ways was the novel in colonial India useful for both the colonisers as well as the
nationalists?

4. Describe how the issue of caste was included in novels in India. By referring to any two
novels, discuss the ways in which they tried to make readers think about existing social
issues.

2. Summarise the concern in both nineteenth-century Europe and India about women
reading novels. What does this suggest about how women were viewed?

5. Describe the ways in which the novel in India attempted to create a sense of pan-Indian
belonging.

3. Explain the following Social changes in Britain which led to an increase in women readers

3. Explain the following What actions of Robinson Crusoe make us see him as a typical coloniser.

3. Explain the following After 1740, the readership of novels began to include poorer people.

3. Explain the following Novelists in colonial India wrote for a political cause.

2. Outline the changes in technology and society which led to an increase in
readers of the novel in eighteenth-century Europe.

3. Write a note on The Oriya novel

3. Write a note on Jane Austen’s portrayal of women

3. Write a note on The picture of the new middle class which the novel Pariksha-Guru portrays.
"""

f = open("jess308_Q.txt", "a+")

string = re.sub("\n\n+", "))))))))", string)

string = re.sub("\n", " ", string)

string = re.sub("\)\)\)\)\)\)\)\)", "\n\n", string)

f.write(string+"\n\n")

f.close()