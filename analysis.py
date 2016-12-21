actual_ham_count=0
actual_spam_count=0
classified_ham_count=0
classified_spam_count=0
correct_ham=0
correct_spam=0
with open('output.txt', "r", encoding="latin1") as f:
    for line in f:
        #print("line:"+line)
        classified = line.split(' ',maxsplit=1)[0]
        #print("classified"+classified)
        if(classified=="ham"):
            classified_ham_count=classified_ham_count+1
        if(classified=="spam"):
            classified_spam_count=classified_spam_count+1
        #print(classified, end=" ")
        path=line.split(' ',maxsplit=1)[1]
        #print("Path:"+path)

        hpath = path
        hfname = hpath.split("\\")
        hcfname = len(hfname)
        hroot_fname = hcfname - 2
        actual=hfname[hroot_fname]
        #print("Actual"+ actual)
        if(actual=="ham"):
            actual_ham_count=actual_ham_count+1
        if(actual=="spam"):
            actual_spam_count=actual_spam_count+1
        if(actual==classified and actual=="ham"):
            correct_ham=correct_ham+1
        if(actual==classified and actual=="spam"):
            correct_spam=correct_spam+1

    print("Classified ham count: " +str(classified_ham_count))
    print("Classified spam count: "+str(classified_spam_count))
    print("Actual ham count: "+str(actual_ham_count))
    print("Actual spam count: "+str(actual_spam_count))
    print("correctly classified as ham: "+str(correct_ham))
    print("correctly classified as spam: "+str(correct_spam))

    accuracy=(correct_ham+correct_spam)/(actual_spam_count+actual_spam_count)
    print("Accuracy: "+str(round(accuracy,2)))

    precision_spam=correct_spam/classified_spam_count
    print("Precesion of spam: "+str(round(precision_spam,2)))

    precision_ham=correct_ham/classified_ham_count
    print("Precision of ham: "+str(round(precision_ham,2)))

    recall_spam=correct_spam/actual_spam_count
    recall_ham=correct_ham/actual_ham_count

    print("Recall of spam: "+str(recall_spam))
    print("Recall of ham: "+str(recall_ham ))

    f1_spam=(2*(precision_spam)*recall_spam)/(precision_spam+recall_spam)
    print("F1 of spam: "+str(round(f1_spam,2)))

    f1_ham=(2*(precision_ham)*recall_ham)/(precision_ham+recall_ham)
    print("F1 of ham: "+str(round(f1_ham,2)))

    tot_file_count=actual_ham_count+actual_spam_count
    #print("Total number of file: "+str(tot_file_count))
    weighted_avg=((actual_ham_count * f1_ham)/tot_file_count)+((actual_spam_count * f1_spam )/tot_file_count)
    print("Weighted Average: "+str(round(weighted_avg,2)))

