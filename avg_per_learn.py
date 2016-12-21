import os,re,random,pickle,sys,time
from collections import defaultdict

#bb=open('test.txt','a+')


# The create_fmap method reads all the files and sub directories and return the fmap which has the key as the path of file and values is the content of the file
def create_fmap(topdir):
    fmap = defaultdict(lambda: "")  # This is the dictionary for the file, file contents
    for root, dirs, files in os.walk(topdir):
        # random.shuffle(dirs)  # for shuffling the directories
        # print("dir: " + str(dirs))
        for file in files:
            # tot=tot+1
            if file.endswith(".txt"):
                fpath = os.path.join(root, file)  # fpath contains the fully qualified path
                # if ("ham" in fpath or "spam" in fpath):
                # print(fpath)  # prints all the files with ham names
                hpath = fpath  # hpath contains path to ham files
                hfname = hpath.split("\\")
                hcfname = len(hfname)
                hroot_fname = hcfname - 2

                if ((hfname[hroot_fname] == "ham") or (hfname[hroot_fname] == "spam")):
                    # y = -1  # if its ham then y=1
                    # print(hpath)
                    hfobj = open(hpath, "r", encoding="latin1")
                    hst = hfobj.read();
                    read_file = hst  # here read_file is the main file thats been considered and we will use this file later in the

                    # remove the \n character from the read file
                    x = read_file.replace("\n", " ")

                    # check if the file name exists in the fmap dictionary, if it doesnt exist then add the file to the dictionary
                    fmap[hpath] = x

                    hfobj.close()  # close the opened file

                    # for hword in read_file.split():
                    #   if (hword not in wcount):  # if the word is present in dictionary means its already been added
                    # alpha += wcount[hword]
                    #       wcount[hword] = 0  # first time initialize the weight to 0 and adding the word to the dictionary
                    #      ucount[hword] = 0

    return fmap



def loop_30(fmap):
    wcount = defaultdict(int)  # wcount is the dictionary for all the words in our model, the key is the word and value is its weight
    ucount = defaultdict(int)

    b = 0
    beta = 0  # This is the avg bias
    count = 1

    for i in range(1, 31):

        # print(i)
        # f.write(str(i))
        keys = list(fmap.keys())
        # random.shuffle(keys)

        for k in keys:
            # tot=tot+1

            # f.write(str(k))
            # f.write(k)
            if k.endswith(".txt"):
                alpha = 0  # re initialize alpha
                y = 0
                # print(k)
                fpath = k  # fpath contains the fully qualified path
                hpath = fpath  # hpath contains path to ham files
                hfname = hpath.split("\\")
                # print(hfname)
                hcfname = len(hfname)
                hroot_fname = hcfname - 2
                if (hfname[hroot_fname] == "ham"):
                    v = fmap[k]
                    # print("ham")
                    y = -1  # if its ham then y=1
                    for hword in v.split():
                        try:
                            alpha += wcount[hword]
                        except KeyError:
                            alpha += 0

                if (hfname[hroot_fname] == "spam"):
                    v = fmap[k]
                    # print(hpath,end=",")
                    y = 1  # if its spam then y=1
                    for sword in v.split():
                        try:
                            alpha += wcount[sword]
                        except KeyError:
                            alpha += 0

                            # for each file we determine the alpha and yalpha respectively
                alpha = alpha + b
                # f.write(" alpha: "+ str(alpha))
                yalpha = y * alpha  # here the y value is updated based on the file respectively
                if (yalpha <= 0):
                    # if (y == -1):  # case for the ham files
                    # print(file,end=' ')
                    # f.write(" y is less than 1 ")
                    # We need to change the weights and bias
                    for word in v.split():
                        # weight_word = wcount[word]
                        # weight_word = weight_word + y  # reduce the weight of word and put it back to the dictionary
                        # wcount[word] = wcount[word] + y  # updating the dictionary with the new weights
                        wcount[word] = wcount[word] + y

                        # for avg weights
                        # avg_weight_word=ucount[word]
                        # avg_weight_word = (avg_weight_word + y*count)
                        # ucount[word]=avg_weight_word
                        ucount[word] = ucount[word] + y * count

                    b = b + y  # update the bias
                    beta = beta + y * count

                    # if (y == 1):  # case for the spam files
                    # print(file, end=' ')
                    # f.write(" y is equals to 1 ")
                    # for word in v.split():
                    # weight_word = wcount[word]
                    # weight_word = weight_word + y  # reduce the weight of word and put it back to the dictionary
                    # wcount[word] = weight_word  # updating the dictionary with the new weights
                    # wcount[word] = wcount[word] + y

                    # for avg weight
                    # avg_weight_word=ucount[word]
                    # avg_weight_word = (avg_weight_word + y*count)
                    # ucount[word]=avg_weight_word
                    # ucount[word] = ucount[word] + y * count

                    # b = b + y  # update the bias
                    # beta=beta+y*count
                    # elif (y == 0):
                    #    continue
                    # print("y is equals to 0")
                    # f.write(" y is equals to 0 ")
                    # elif (yalpha > 0):
                    # f.write(" y alpha is greater than 0 so no change")
                    # continue
                count = count + 1
                # print("The count value is "+str(count))

    wcount["var_bias"] = b

    for key in ucount:
        # val=ucount[key]
        # w=wcount[key]
        # u=(w - (1/count)*val)
        ucount[key] = wcount[key] - (1 / count) * ucount[key]

    # f.write("\n Final model:\n"+str(ucount))

    beta = (b - (1 / count) * beta)

    ucount["var_avg_bias"] = beta

    Mydny = [wcount, ucount]
    f = open('per_model.txt', 'wb')
    pickle.dump(Mydny, f)
    # print("B is: "+str(wcount["var_bias"]) )
    # print("\nBeta is:"+str(ucount["var_avg_bias"]))


    return





#code for main program
starttime=time.time()
topdir = 'C:\\Users\\Arjun\\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment1\\Spam or Ham\\train'
#topdir=sys.argv[1]     #This is for the command line to be added later

#topdir ="C:\\Users\\Arjun\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment2\\10_percnt_data"

fmap=create_fmap(topdir)
loop_30(fmap)

print("--- %s seconds ---" % (time.time() - starttime))