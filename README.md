Multiprocessing with both Pool and Manager+Queue approach demonstrated better results than standard approach. Multi-threading didn't provide any better result. Copy of execution output is provided below:


Approach:                               | Time
----------------------------------------|-----
Standard approach:                      | 5.363
Multi-threading approach:               | 5.500
Multi-process/Pool approach:            | 4.512
Multi-process/Manager+Queue approach:   | 4.110

Results of searches:

Standard approach results == Multi-threading approach results

Standard approach results == Multi-process/Pool approach results

Standard approach results == Multi-process/Manager+Queue approach results

Results of the search:

compose: ['.\\texts\\text1.txt', '.\\texts\\text2.txt', '.\\texts\\text3.txt', '.\\texts\\text4.txt', '.\\texts\\text5.txt', '.\\texts\\text6.txt'] 

agriculture: []

surname: ['.\\texts\\text1.txt', '.\\texts\\text2.txt', '.\\texts\\text4.txt', '.\\texts\\text5.txt']

legislation: []

difference: ['.\\texts\\text1.txt', '.\\texts\\text2.txt', '.\\texts\\text3.txt', '.\\texts\\text4.txt', '.\\texts\\text5.txt']

math: ['.\\texts\\text5.txt']

list: ['.\\texts\\text1.txt', '.\\texts\\text2.txt', '.\\texts\\text3.txt', '.\\texts\\text4.txt', '.\\texts\\text5.txt', '.\\texts\\text6.txt']    

introduction: ['.\\texts\\text1.txt', '.\\texts\\text2.txt', '.\\texts\\text3.txt', '.\\texts\\text4.txt', '.\\texts\\text5.txt']

annotation: []

composition: ['.\\texts\\text1.txt', '.\\texts\\text2.txt', '.\\texts\\text3.txt', '.\\texts\\text4.txt', '.\\texts\\text5.txt']
