# CS839

All Documents: [Set B](https://github.com/swatianand56/CS839/tree/master/Stage_1/B)

Training Documents: [Set I](https://github.com/swatianand56/CS839/tree/master/Stage_1/I)

Testing Documents: [Set J](https://github.com/swatianand56/CS839/tree/master/Stage_1/J)

[Code](https://github.com/swatianand56/CS839/tree/master/Stage_1)

### Setup:
Install the requirements mentioned in `requirements.txt` (`docopt`, `pandas` and `sklearn`)
or you have `pip` setup, you may do `pip install --user -r requirements.txt`

Make sure you have `python 3` setup

In order to run the code,
```
./run.sh
```
This will install the requirements (mentioned in `requirements.txt` file), tokenize (on training data I and testing data J)
and run on Neural Network Classifier.

### API Documentation:

```
CS839 (Stage 1) API

Usage:
    main.py [--shuffle]
    main.py -h | --help
    main.py run [<classifiers>] [--kfold]

Options:
    -h --help     : Generates test and train data for files from 1-200 and 201-300 by default.
                    Classifiers -
                    Decision Tree(DT), Support Vector Machine (SVM), Random Forest (RF)
                    Neural Netword (NN), Logistic Regression (LOR), Linear Regresssion (LR)

    --shuffle     : Generates test and train data by randomly choosing 100 files and 200 files.
    --kfold       : Run Cross Validation
    <classifiers> : Classifiers on which you wish to run (DT, SVM, RF, NN, LOR, LR)
````


#### Generating the training and test data feature vector:
```
python3 main.py
```
This only generates `train.csv` and `test.csv` files containing the feature vectors of training and testing data.
Note: The training data is generated from train files (101-300 in folder [I](https://github.com/swatianand56/CS839/tree/master/Stage_1/I)) and testing data is generated from
test files (1-100 in folder [J](https://github.com/swatianand56/CS839/tree/master/Stage_1/J))

![Generate I and J](images/generateIJ.png?raw=true "Generate I and J")


###### (Optional) Generating the training and test data feature vector if you want to generate the train and test by randomly choosing 200/100 train/test files rather than fixed from I and J):


```
python3 main.py --shuffle
```
![Shuffle on B to generate I and J](images/shuffle.png?raw=true "Shuffle on B to generate I and J")


#### Running on all the classifiers
```
python3 main.py run
```
This will run on all classifiers namely Decision Tree(DT), Support Vector Machine (SVM), Random Forest (RF), Neural Netword (NN), Logistic Regression (LOR), Linear Regresssion (LR) with training set I and testing set J

![Run All](images/runAll.png?raw=true "Run All")

However, if you want to try running on any of those, you may run
```
python3 main.py run <classifiers>
```
where `<classifiers>` can be written as "NN, DT" or any classifiers you choose to run on. For example, `python3 main.py run "NN, DT, RF"`

#### Running Cross Validation on Set I
```
python3 main.py run "NN" --kfold
```
![Neural Network K-Fold on I](images/NNfold.png?raw=true "Neural Network K-Fold on I")

