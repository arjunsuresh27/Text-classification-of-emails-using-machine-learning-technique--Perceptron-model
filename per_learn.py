import os,sys,re,random,pickle,time
from collections import defaultdict

def create_fmap(topdir):
    fmap = defaultdict(lambda: "")  # This is the dictionary for the file, file contents

    for root, dirs, files in os.walk(topdir):
        # print(len(files))
        # print(len(dirs))
        random.shuffle(dirs)  # for shuffling the directories
        # print("dir: " + str(dirs))

        for file in files:
            #tot = tot + 1
            if file.endswith(".txt"):
                fpath = os.path.join(root, file)  # fpath contains the fully qualified path
                # if ("ham" in fpath or "spam" in fpath):
                # print(fpath)  # prints all the files with ham names
                hpath = fpath  # hpath contains path to ham files
                hfname = hpath.split("\\")
                hcfname = len(hfname)
                hroot_fname = hcfname - 2
                if ((hfname[hroot_fname].lower() == "ham") or (hfname[hroot_fname].lower() == "spam")):
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
                    # create a file to write nbmodel.txt
                    # f = open('per_model.txt', 'a+', encoding="latin1")  # open the file in append mode
                    # f.write("ham,")
                    # f.write(hpath+",")
                    # print("ham,", end=""),  # printing at end of file as spam or ham
                    # print(read_file)
                    # for hword in read_file.split():
                    #    if (hword not in wcount):  # if the word is present in dictionary means its already been added
                    #        #alpha += wcount[hword]
                    #       wcount[hword] = 0# first time initialize the weight to 0 and adding the word to the dictionary

    return fmap





#print(wcount)
#f.write("Before")
#f.write(str(wcount))
#print(fmap)
#f.write(str(fmap))




def loop_20(fmap):
    b = 0
    wcount = defaultdict(int)  # wcount is the dictionary for all the words in our model, the key is the word and value is its weight

    for i in range(1, 21):

        # print(i)
        # f.write(str(i))
        # tot=0
        keys = list(fmap.keys())
        random.shuffle(keys)

        for k in keys:
            # tot=tot+1
            v = fmap[k]
            # f.write(str(tot)+ " file: " +str(k)+" data "+str(fmap[k])+ "\n")
            # f.write(k)
            if k.endswith(".txt"):
                alpha = 0  # re initialize alpha
                y = 0
                # print(k)
                fpath = k  # fpath contains the fully qualified path
                # ("ham" in fpath):
                # print(fpath)  # prints all the files with ham names
                hpath = fpath  # hpath contains path to ham files
                hfname = hpath.split("\\")
                # print(hfname)
                hcfname = len(hfname)
                hroot_fname = hcfname - 2
                if (hfname[hroot_fname] == "ham"):
                    # print("ham")
                    y = -1  # if its ham then y=1
                    for hword in v.split():
                        try:
                            alpha += wcount[hword]
                        except KeyError:
                            alpha += 0
                # ("spam" in fpath):
                # print(fpath)  # prints all the file names with spam names
                # spath = fpath
                # sfname = spath.split("\\")
                # scfname = len(sfname)
                # sroot_fname = scfname - 2
                if (hfname[hroot_fname] == "spam"):
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
                    if (y == -1):  # case for the ham files
                        # print(file,end=' ')
                        # f.write(" y is less than 1 ")
                        # We need to change the weights and bias
                        for word in v.split():
                            weight_word = wcount[word]
                            weight_word = weight_word + y  # reduce the weight of word and put it back to the dictionary
                            wcount[word] = weight_word  # updating the dictionary with the new weights
                        b = b + y  # update the bias
                    if (y == 1):  # case for the spam files
                        # print(file, end=' ')
                        # f.write(" y is equals to 1 ")
                        for word in v.split():
                            weight_word = wcount[word]
                            weight_word = weight_word + y  # reduce the weight of word and put it back to the dictionary
                            wcount[word] = weight_word  # updating the dictionary with the new weights
                        b = b + y  # update the bias
                        # elif (y == 0):
                        #    continue
                        # print("y is equals to 0")
                        # f.write(" y is equals to 0 ")
                        # elif (yalpha > 0):
                        # f.write(" y alpha is greater than 0 so no change")
                        #    continue

    # need to add this
    wcount["var_bias"] = b  # adding the bias to the dictionary and into the file which is used in the classifier respectively
    Mydny = [wcount]  # using the list of dictionary to dump the dictionalry into the pickle file
    f = open('per_model.txt', 'wb')
    pickle.dump(Mydny, f)  # use pickle to finally dump the dictionary to the model.txt file





    return


#run for 20 iterations


#f.write("\nAfter loop\n")
#f.write(str(wcount))
#f.write("\n"+str(tot))
#print(" b: "+str(b))
#print("There is b in dictionary is: "+str(wcount["b"]))




#Begin of main code

starttime=time.time()
topdir = 'C:\\Users\\Arjun\\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment1\\Spam or Ham\\train'

#topdir ="C:\\Users\\Arjun\Desktop\\USC\\Subjets\\fall2016\\csci544\\Assignment2\\10_percnt_data"

#topdir=sys.argv[1]     #This is for the command line to be added later
fmap=create_fmap(topdir)
loop_20(fmap)

print("--- %s seconds ---" % (time.time() - starttime))