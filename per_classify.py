import os,sys,codecs,re,random,pickle, time, warnings



starttime=time.time()

actual_ham_count = 0
actual_spam_count = 0
classified_ham_count = 0
classified_spam_count = 0
correct_ham = 0
correct_spam = 0


f=open("per_model.txt","rb")
Mydny=pickle.load(f)
#print(str(wcount))
size=len(Mydny)
if(size==1):
    wcount=Mydny[0]
    #print("Standard algo")
if(size==2):
    #print("Weighted algo")
    wcount=Mydny[0]
    ucount=Mydny[1]

#outfile=sys.argv[2]
outfile="output.txt"
op=open(outfile,"a+")


def analyser():
    print("Analysis Report " )
    print("Classified ham count: " + str(classified_ham_count))
    print("Classified spam count: " + str(classified_spam_count))
    print("Actual ham count: " + str(actual_ham_count))
    print("Actual spam count: " + str(actual_spam_count))
    print("correctly classified as ham: " + str(correct_ham))
    print("correctly classified as spam: " + str(correct_spam))
    accuracy = (correct_ham + correct_spam) / (actual_spam_count + actual_spam_count)
    print("Accuracy: " + str(round(accuracy, 2)))
    precision_spam = correct_spam / classified_spam_count
    print("Precesion of spam: " + str(round(precision_spam, 2)))
    precision_ham = correct_ham / classified_ham_count
    print("Precision of ham: " + str(round(precision_ham, 2)))
    recall_spam = correct_spam / actual_spam_count
    recall_ham = correct_ham / actual_ham_count
    print("Recall of spam: " + str(round(recall_spam,2)))
    print("Recall of ham: " + str(round(recall_ham,2)))
    f1_spam = (2 * (precision_spam) * recall_spam) / (precision_spam + recall_spam)
    print("F1 of spam: " + str(round(f1_spam, 2)))
    f1_ham = (2 * (precision_ham) * recall_ham) / (precision_ham + recall_ham)
    print("F1 of ham: " + str(round(f1_ham, 2)))
    tot_file_count = actual_ham_count + actual_spam_count
    # print("Total number of file: "+str(tot_file_count))
    weighted_avg = ((actual_ham_count * f1_ham) / tot_file_count) + ((actual_spam_count * f1_spam) / tot_file_count)
    print("Weighted Average: " + str(round(weighted_avg, 2)))
    print(" ")


    return




def classifier(fpath):
    global actual_ham_count
    global actual_spam_count
    global correct_ham
    global correct_spam
    global classified_ham_count
    global classified_spam_count


    if(size==1):

        hpath = fpath
        hfname = hpath.split("\\")
        hcfname = len(hfname)
        hroot_fname = hcfname - 2
        actual = hfname[hroot_fname]

        #print("Standard algo")
        alpha = 0  # initialize alpha to 0
        b = wcount["var_bias"]  # retrieve the bias value stored in the dictionary
        # print(str(b))
        hfobj = open(fpath, "r", encoding="latin1")
        hst = hfobj.read()
        hfobj.close()
        for word in re.sub('\s\s+', ' ', hst).strip().split():
            if word in wcount:
                alpha += wcount[word]




            else:
                continue  # case when the word in test data is not present in our model, we just ignore the word!! No smoothing here

        if ((alpha + b) > 0):
            # print(fpath+" SPAM " +" alpha is: "+str(alpha)+" b is "+str(b))
            op.write("spam " + fpath)
            classified="spam"



        else:
            # print(fpath+" HAM "+" alpha is: "+str(alpha+b)+" b is "+str(b))
            op.write("ham " + fpath)
            classified="ham"

        if (actual == "ham"):
            #global actual_ham_count
            actual_ham_count = actual_ham_count + 1
        if (actual == "spam"):
            #global actual_spam_count
            actual_spam_count = actual_spam_count + 1
        if (actual == classified and actual == "ham"):
            #global correct_ham
            correct_ham = correct_ham + 1
        if (actual == classified and actual == "spam"):
            #global  correct_spam
            correct_spam = correct_spam + 1

        if (classified == "ham"):
            #global classified_ham_count
            classified_ham_count = classified_ham_count + 1
        if (classified == "spam"):
            #global classified_spam_count
            classified_spam_count = classified_spam_count + 1


        op.write("\n")


    if(size==2):
        hpath = fpath
        hfname = hpath.split("\\")
        hcfname = len(hfname)
        hroot_fname = hcfname - 2
        actual = hfname[hroot_fname]


        #print("Weighted algo")
        alpha = 0  # initialize alpha to 0
        #b = wcount["var_bias"]  # retrieve the bias value stored in the dictionary
        beta=ucount["var_avg_bias"]
        # print(str(b))
        hfobj = open(fpath, "r", encoding="latin1")
        hst = hfobj.read()
        hfobj.close()
        for word in re.sub('\s\s+', ' ', hst).strip().split():
            if word in wcount:
                alpha += ucount[word]




            else:
                continue  # case when the word in test data is not present in our model, we just ignore the word!! No smoothing here

        if ((alpha + beta) > 0):
            # print(fpath+" SPAM " +" alpha is: "+str(alpha)+" b is "+str(b))
            op.write("spam " + fpath)
            classified = "spam"



        else:
            # print(fpath+" HAM "+" alpha is: "+str(alpha+b)+" b is "+str(b))
            op.write("ham " + fpath)
            classified = "ham"

        if (actual == "ham"):
            #global actual_ham_count
            actual_ham_count = actual_ham_count + 1
        if (actual == "spam"):
            #global actual_spam_count
            actual_spam_count = actual_spam_count + 1
        if (actual == classified and actual == "ham"):
            #global correct_ham
            correct_ham = correct_ham + 1
        if (actual == classified and actual == "spam"):
            #global  correct_spam
            correct_spam = correct_spam + 1

        if (classified == "ham"):
            #global classified_ham_count
            classified_ham_count = classified_ham_count + 1
        if (classified == "spam"):
            #global classified_spam_count
            classified_spam_count = classified_spam_count + 1


        op.write("\n")

    return




topdir = 'C:\\Users\\Arjun\\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment2\\Spam or Ham\\dev'              #path to the Development data



#topdir=sys.argv[1]
#print(topdir)
exten = '.txt'
for root, dirs, files in os.walk(topdir):
    for file in files:
        if file.endswith(".txt"):
            fpath = os.path.join(root, file)  # fpath contains the fully qualified path
            classifier(fpath)



analyser()
#print("--- %s seconds ---" % (time.time() - starttime))


