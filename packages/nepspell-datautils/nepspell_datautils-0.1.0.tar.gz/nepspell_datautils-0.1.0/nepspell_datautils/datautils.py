"""
    1. Pseudo random word and character level insertion, substitution, deletion, or shuffling operations
"""


"""
    re: for regular expression

"""



import re
import random
import math
import csv
import os
import pandas as pd
import glob

"""
    Working with character level error.
    A character is 
        1. deleted 
        2. inserted
        4. replaced by another character
"""

def wordsWithCharacter(sentence,character):
    """
        To select the words that have the character in the sentence.
    """
    return [word for word in sentence.split() if character in word]

def positionsOfCharacter(sentence,character):
    """
        To get the positions where the characters is present.
    """
    return [index for index, char in enumerate(sentence) if char == character]

def replaceCharacterAt(sentence, index, charOut):
    """
        The charOut is place at the index replacing the old character.
    """
    return sentence[:index] + charOut + sentence[index + 1:]

def deleteCharacterAt(sentence, index):
    """
        Delete or remove the character at the index.
        The character at the index may be whitespace or any other character
    """
    return sentence[:index] + sentence[index + 1:]

def addCharacterAt(sentence, index, charOut):
    """
        The charOut is added at the index.
    """
    return sentence[:index] + charOut + sentence[index + 1:]

"""
    Working with word level or word sequence
    A sequence or word may be 
        1. replaced by another word or character sequence
        2. deleted
        3. added
"""
def wordsWithCharSeq(sentence,charSeq):
    """
        Returns the words with the charSeq in the sentence.
    """
    return [word for word in sentence.split() if charSeq in word]

def positionsOfCharSeq(sentence,charSeq):
    """
        Returns the positions of the charSeq in the sentence
    """
    occurrences = []
    for match in re.finditer(charSeq, sentence):
        # Access the starting index of the match object
        index = match.start()
        occurrences.append(index)
    return occurrences

def replaceCharSeqAt(sentence, index, charSeqIn, charSeqOut):
    """
        Replace the charSeqIn at index by charSeqOut in the sentence.
    """
   # Extract parts before and after the index
    before = sentence[:index]
    after = sentence[index + len(charSeqIn):]
    # Combine the parts with the replacement
    return before + charSeqOut + after

def deleteCharSeqAt(sentence, index, charSeqIn):
    """
        Delete the charSeqIn at index in the sentence.
    """
   # Extract parts before and after the index
    before = sentence[:index]
    after = sentence[index + len(charSeqIn):]
    # Combine the remaining parts
    return before + after

def addCharSeqAt(sentence, index, charSeqOut):
    """
        Add the charSeqOut at index in the sentence.
    """
   # Extract parts before and after the index
    before = sentence[:index]
    after = sentence[index:]
    # Combine the remaining parts
    return before + charSeqOut + after


############################################################


"""
    1. Single Error Type Per sentence
    2. MaxErrorCount for maximum of such error type in a sentence
    3. TotalDatapoints of sentences with such error type
"""

def characterReplaceType(sentences, charIn, charOut, maxErrorCount = 1, totalDataPoints = 1 ):
    """
    Generates a dictionary containing correct and incorrect sentence pairs with random errors introduced.

    Args:
        sentences (List[str]): A list of original sentences.
        charIn (str): The character to replace or introduce errors on.
        charOut (str): The character to use for replacements or deletions.
        maxErrorCount (int, optional): The maximum number of errors to introduce per sentence. Defaults to 1.
        totalDataPoints (int, optional): The desired number of total data points (correct-incorrect pairs). Defaults to 1.

    Returns:
        dict: A dictionary with two keys:
            - "Correct": A list of sentences containing the original character (`charIn`).
            - "Incorrect": A list of sentences with random errors introduced.
    """

    # Shuffle the list 
    random.shuffle(sentences)
    
    inSentences=[]
    outSentences =[]
    
    if(len(sentences)!=0): # input sentences is not empty
        datapointsCount=0
        for sentence in sentences: # iterate through all the sentences
            if(len(positionsOfCharacter(sentence,charIn))!=0): # contain the character to be replaced
                inSentences.append(sentence)
                availablePositions = positionsOfCharacter(sentence,charIn)

                # Determine number of errors randomly based on max_error_count and available positions
                errorCount = random.randint(1, min(maxErrorCount, len(availablePositions)))
                errorPositions=random.sample(availablePositions,errorCount)
                modifiedSentence = sentence[:]
                
                for index in errorPositions:
                    modifiedSentence = replaceCharacterAt(modifiedSentence,index,charOut)

                outSentences.append(modifiedSentence)
                datapointsCount+=1
                
            if (datapointsCount==totalDataPoints):
                break
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }
    else:
        print("Sentences List is EMPTY")
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }

def characterDeleteType(sentences, charIn, maxErrorCount = 1, totalDataPoints = 1):
    """
    Generates a dictionary containing correct and incorrect sentence pairs with random character deletions.

    Args:
        sentences (List[str]): A list of original sentences.
        charIn (str): The character to delete.
        maxErrorCount (int, optional): The maximum number of deletions per sentence. Defaults to 1.
        totalDataPoints (int, optional): The desired number of total data points (correct-incorrect pairs). Defaults to 1.

    Returns:
        dict: A dictionary with two keys:
            - "Correct": A list of original sentences containing the given character.
            - "Incorrect": A list of sentences with random character deletions.
    """

    # Shuffle the list 
    random.shuffle(sentences)

    inSentences=[]
    outSentences =[]
    
    if(len(sentences)!=0):
        datapointsCount=0
        for sentence in sentences:
            if(len(positionsOfCharacter(sentence,charIn))!=0):
                inSentences.append(sentence)

                availablePositions = positionsOfCharacter(sentence,charIn)

                # Determine number of errors randomly based on max_error_count and available positions
                errorCount = random.randint(1, min(maxErrorCount, len(availablePositions)))
                errorPositions=random.sample(availablePositions,errorCount)
                modifiedSentence = sentence[:]
                
                for index in errorPositions:
                    modifiedSentence = deleteCharacterAt(modifiedSentence,index)

                outSentences.append(modifiedSentence)
                datapointsCount+=1
                
            if (datapointsCount==totalDataPoints):
                break
        return {
            "Correct":inSentences,
            "Incorrect": outSentences
        }
    else:
        print("Sentences List is EMPTY")
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }

def characterAddType(sentences, charOut, maxErrorCount = 1, totalDataPoints = 1 ):
    """
    Generates a dictionary containing correct and incorrect sentence pairs with random character insertions.

    Args:
        sentences (List[str]): A list of original sentences.
        charOut (str): The character to insert.
        maxErrorCount (int, optional): The maximum number of insertions per sentence. Defaults to 1.
        totalDataPoints (int, optional): The desired number of total data points (correct-incorrect pairs). Defaults to 1.

    Returns:
        dict: A dictionary with two keys:
            - "Correct": A list of original sentences.
            - "Incorrect": A list of sentences with random character insertions.
    """

    # Shuffle the list 
    random.shuffle(sentences)
    
    inSentences=[]
    outSentences =[]
    
    if(len(sentences)!=0): # input sentences is not empty
        datapointsCount=0
        for sentence in sentences: # iterate through all the sentences
            if(len(sentence)!=0): # contain the character to be replaced
                inSentences.append(sentence)
                # Determine number of errors randomly based on max_error_count and available positions
                errorCount = random.randint(1,math.floor(0.025 * len(sentence)) )
                errorPositions=random.sample(range(len(sentence)),errorCount)
                modifiedSentence = sentence[:]
                
                for index in errorPositions:
                    modifiedSentence = addCharacterAt(modifiedSentence,index,charOut)

                outSentences.append(modifiedSentence)
                datapointsCount+=1
                
            if (datapointsCount==totalDataPoints):
                break
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }
    else:
        print("Sentences List is EMPTY")
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }

def characterSeqReplaceType(sentences, charSeqIn, charSeqOut, maxErrorCount = 1, totalDataPoints = 1 ):
    """
    Generates a dictionary containing correct and incorrect sentence pairs with random character sequence replacements.

    Args:
        sentences (List[str]): A list of original sentences.
        charSeqIn (str): The character sequence to replace.
        charSeqOut (str): The character sequence to use for replacements.
        maxErrorCount (int, optional): The maximum number of replacements per sentence. Defaults to 1.
        totalDataPoints (int, optional): The desired number of total data points (correct-incorrect pairs). Defaults to 1.

    Returns:
        dict: A dictionary with two keys:
            - "Correct": A list of sentences containing the original character sequence (`charSeqIn`).
            - "Incorrect": A list of sentences with random character sequence replacements.
    """

    # Shuffle the list 
    random.shuffle(sentences)
    
    inSentences=[]
    outSentences =[]
    
    if(len(sentences)!=0): # input sentences is not empty
        datapointsCount=0
        for sentence in sentences: # iterate through all the sentences
            if(len(positionsOfCharSeq(sentence,charSeqIn))!=0): # contain the character to be replaced
                inSentences.append(sentence)
                availablePositions = positionsOfCharSeq(sentence,charSeqIn)

                # Determine number of errors randomly based on max_error_count and available positions
                errorCount = random.randint(1, min(maxErrorCount, len(availablePositions)))
                errorPositions=random.sample(availablePositions,errorCount)
                modifiedSentence = sentence[:]
                
                for index in errorPositions:
                    modifiedSentence = replaceCharSeqAt(modifiedSentence,index,charSeqIn,charSeqOut)

                outSentences.append(modifiedSentence)
                datapointsCount+=1
                
            if (datapointsCount==totalDataPoints):
                break
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }
    else:
        print("Sentences List is EMPTY")
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }

def characterSeqDeleteType(sentences, charSeqIn, maxErrorCount = 1, totalDataPoints = 1):
    """
    Generates a dictionary containing correct and incorrect sentence pairs with random character sequence deletions.

    Args:
        sentences (List[str]): A list of original sentences.
        charSeqIn (str): The character sequence to delete.
        maxErrorCount (int, optional): The maximum number of deletions per sentence. Defaults to 1.
        totalDataPoints (int, optional): The desired number of total data points (correct-incorrect pairs). Defaults to 1.

    Returns:
        dict: A dictionary with two keys:
            - "Correct": A list of sentences containing the original character sequence.
            - "Incorrect": A list of sentences with random character sequence deletions.
    """

    # Shuffle the list 
    random.shuffle(sentences)

    inSentences=[]
    outSentences =[]
    
    if(len(sentences)!=0):
        datapointsCount=0
        for sentence in sentences:
            if(len(positionsOfCharSeq(sentence,charSeqIn))!=0):
                inSentences.append(sentence)

                availablePositions = positionsOfCharSeq(sentence,charSeqIn)

                # Determine number of errors randomly based on max_error_count and available positions
                errorCount = random.randint(1, min(maxErrorCount, len(availablePositions)))
                errorPositions=random.sample(availablePositions,errorCount)
                modifiedSentence = sentence[:]
                
                for index in errorPositions:
                    modifiedSentence = deleteCharSeqAt(modifiedSentence,index,charSeqIn)

                outSentences.append(modifiedSentence)
                datapointsCount+=1
                
            if (datapointsCount==totalDataPoints):
                break
        return {
            "Correct":inSentences,
            "Incorrect": outSentences
        }
    else:
        print("Sentences List is EMPTY")
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }

def characterSeqAddType(sentences, charSeqOut, maxErrorCount = 1, totalDataPoints = 1 ):
    """
    Generates a dictionary containing correct and incorrect sentence pairs with random character sequence insertions.

    Args:
        sentences (List[str]): A list of original sentences.
        charOut (str): The character sequence to insert (can be a single character or a string).
        maxErrorCount (int, optional): The maximum number of insertion points per sentence.
            Defaults to 1 (unlimited).
        totalDataPoints (int, optional): The desired number of total data points
            (correct-incorrect pairs). Defaults to 1 (all possible combinations).

    Returns:
        dict: A dictionary with two keys:
            - "Correct": A list of original sentences.
            - "Incorrect": A list of sentences with random character sequence insertions.
    """
    # Shuffle the list 
    random.shuffle(sentences)
    
    inSentences=[]
    outSentences =[]
    
    if(len(sentences)!=0): # input sentences is not empty
        datapointsCount=0
        for sentence in sentences: # iterate through all the sentences
            if(len(sentence)!=0): # contain the character to be replaced
                inSentences.append(sentence)
                # Determine number of errors randomly based on max_error_count and available positions
                errorCount = random.randint(1,math.floor(0.025 * len(sentence)) )
                errorPositions=random.sample(range(len(sentence)),errorCount)
                modifiedSentence = sentence[:]
                
                for index in errorPositions:
                    modifiedSentence = addCharSeqAt(modifiedSentence,index,charSeqOut)

                outSentences.append(modifiedSentence)
                datapointsCount+=1
                
            if (datapointsCount==totalDataPoints):
                break
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }
    else:
        print("Sentences List is EMPTY")
        return {
                    "Correct":inSentences,
                    "Incorrect": outSentences
                }


"""
    1. Put the outputs to the corresponding csv files
    2. Save the csv file to ./outputfiles/
    3. Track the count of each type generated on parisGenerated
"""
pairsGenerated= []

def characterReplaceTypeToCSV(sentences, charIn, charOut, totalDatapoints):
    """
    Generates a CSV file containing correct and incorrect sentence pairs with random character replacements.

    Args:
        sentences (List[str]): A list of original sentences.
        charIn (str): The character to replace.
        charOut (str): The character to use for replacements.
        totalDatapoints (int): The desired number of total data points (correct-incorrect pairs).
    
    Returns:
        None
    """
    maxErrorCount = 3
    outputSentencesDict = characterReplaceType(sentences, charIn, charOut, maxErrorCount ,totalDatapoints)

    if outputSentencesDict is not None:
        outputFile = f"./outputfiles/{len(outputSentencesDict['Correct'])}-{charIn}-replacedBy-{charOut}.csv"
        with open(outputFile, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)

            # Write the values
            for correctSentence, incorrectSentence in zip(outputSentencesDict['Correct'], outputSentencesDict['Incorrect']):
                csvWriter.writerow([correctSentence, incorrectSentence])
        pairsGenerated.append(len(outputSentencesDict["Correct"]))
        print(f"CSV file '{outputFile}' has been created.")
    else:
        print(f"No data points generated for character '{charIn}-replacedBy-{charOut}'.")

def characterDeleteTypeToCSV(sentences, charIn, totalDatapoints):
    """
    Generates a CSV file containing correct and incorrect sentence pairs with random character deletions.

    Args:
        sentences (List[str]): A list of original sentences.
        characterIn (str): The character to delete.
        totalDataPoints (int): The desired number of total data points (correct-incorrect pairs).

    Returns:
        None
    """
    maxErrorCount = 3
    outputSentencesDict = characterDeleteType(sentences, charIn, maxErrorCount, totalDatapoints)
    
    if outputSentencesDict is not None:
        outputFileName = f'{len(outputSentencesDict["Correct"])}-{charIn}-deleted.csv'
        with open(outputFileName,'w',newline='') as csv_file:
            csvWriter=csv.writer(csv_file)
            # Write the values
            for correctSentence, incorrectSentence in zip(outputSentencesDict["Correct"], outputSentencesDict["Incorrect"]):
                csvWriter.writerow([correctSentence, incorrectSentence])
                
        pairsGenerated.append(len(outputSentencesDict["Correct"]))
        print(f"CSV file '{outputFileName}' has been created.")
    else:
        print(f"No data points generated for character '{charIn}' deleted.")

def characterAddTypeToCSV(sentences,charOut,totalDatapoints):
    """
    Generates a CSV file containing correct and incorrect sentence pairs with random character insertions.

    Args:
        input_sentences (List[str]): A list of original sentences.
        character_out (str): The character to insert.
        total_data_points (int): The desired number of total data points (correct-incorrect pairs).

    Returns:
        None (data written to CSV file)
    """
    maxErrorCount = 3
    outputSentencesDict = characterAddType(sentences,charOut,maxErrorCount,totalDatapoints)
    
    if outputSentencesDict is not None:
        outputFileName = f'{len(outputSentencesDict["Correct"])}-{charOut}-Added_.csv'
        with open(outputFileName,'w',newline='') as csv_file:
            csvWriter=csv.writer(csv_file)
            # Write the values
            for correct_sentence, incorrect_sentence in zip(outputSentencesDict["Correct"], outputSentencesDict["Incorrect"]):
                csvWriter.writerow([correct_sentence, incorrect_sentence])
        pairsGenerated.append(len(outputSentencesDict["Correct"]))
        print(f"CSV file '{outputFileName}' has been created.")
    else:
        print(f"No data points generated for character '{charOut}-Added'.")
        
def characterSeqReplaceTypeToCSV(sentences, charSeqIn, charSeqOut, totalDatapoints):
    """
    Generates a CSV file containing correct and incorrect sentence pairs with random character sequence replacements.

    Args:
        input_sentences (List[str]): A list of original sentences.
        char_seq_in (str): The character sequence to replace.
        char_seq_out (str): The character sequence to use for replacements.
        total_data_points (int): The desired number of total data points (correct-incorrect pairs).

    Returns:
        None (data written to CSV file)
    """
    
    maxErrorCount = 3
    outputSentencesDict = characterSeqReplaceType(sentences, charSeqIn, charSeqOut, maxErrorCount ,totalDatapoints)

    if outputSentencesDict is not None:
        outputFile = f"./outputfiles/{len(outputSentencesDict['Correct'])}-{charSeqIn}-replacedBy-{charSeqOut}.csv"
        with open(outputFile, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile)

            # Write the values
            for correctSentence, incorrectSentence in zip(outputSentencesDict['Correct'], outputSentencesDict['Incorrect']):
                csvWriter.writerow([correctSentence, incorrectSentence])
        pairsGenerated.append(len(outputSentencesDict["Correct"]))
        print(f"CSV file '{outputFile}' has been created.")
    else:
        print(f"No data points generated for character '{charSeqIn}-replacedBy-{charSeqOut}'.")

def characterSeqDeleteTypeToCSV(sentences, charSeqIn, totalDatapoints):
    """
    Generates a CSV file containing correct and incorrect sentence pairs with random character sequence deletions.

    Args:
        input_sentences (List[str]): A list of original sentences.
        character_seq_in (str): The character sequence to delete.
        total_data_points (int): The desired number of total data points (correct-incorrect pairs).

    Returns:
        None (data written to CSV file)
    """
    maxErrorCount = 3
    outputSentencesDict = characterSeqDeleteType(sentences, charSeqIn, maxErrorCount, totalDatapoints)
    
    if outputSentencesDict is not None:
        outputFileName = f'./outputfiles/{len(outputSentencesDict["Correct"])}-{charSeqIn}-deleted.csv'
        with open(outputFileName,'w',newline='') as csv_file:
            csvWriter=csv.writer(csv_file)
            # Write the values
            for correctSentence, incorrectSentence in zip(outputSentencesDict["Correct"], outputSentencesDict["Incorrect"]):
                csvWriter.writerow([correctSentence, incorrectSentence])
                
        pairsGenerated.append(len(outputSentencesDict["Correct"]))
        print(f"CSV file '{outputFileName}' has been created.")
    else:
        print(f"No data points generated for character '{charSeqIn}' deleted.")

def characterSeqAddToType(sentences,charSeqOut,totalDatapoints):
    """
    Generates a CSV file containing correct and incorrect sentence pairs with random character insertions.

    Args:
        input_sentences (List[str]): A list of original sentences.
        character_out (str): The character to insert.
        total_data_points (int): The desired number of total data points (correct-incorrect pairs).

    Returns:
        None (data written to CSV file)
    """
    maxErrorCount = 3
    outputSentencesDict = characterAddType(sentences,charSeqOut,maxErrorCount,totalDatapoints)
    
    if outputSentencesDict is not None:
        outputFileName = f'./outputfiles/{len(outputSentencesDict["Correct"])}-{charSeqOut}-Added_.csv'
        with open(outputFileName,'w',newline='') as csv_file:
            csvWriter=csv.writer(csv_file)
            # Write the values
            for correct_sentence, incorrect_sentence in zip(outputSentencesDict["Correct"], outputSentencesDict["Incorrect"]):
                csvWriter.writerow([correct_sentence, incorrect_sentence])
        pairsGenerated.append(len(outputSentencesDict["Correct"]))
        print(f"CSV file '{outputFileName}' has been created.")
    else:
        print(f"No data points generated for character '{charSeqOut}-Added'.")
        

"""
    Creating datapoints for sentences using the config files.
"""
def characterReplaceDatapoints(sentences, characterReplaceConfig):
    """
    This function replaces characters in each sentence from the `sentences` list with other
    specified characters based on the configuration provided in `characterReplaceConfig`.

    Args:
        sentences: A list of strings representing the sentences to process.
        characterReplaceConfig: A list of tuples where each tuple contains:
            - The character to be replaced (charIn).
            - The replacement character (charOut).
            - The number of datapoints to generate (totalDatapoints).

    Returns:
        None. The function modifies the `sentences` list in-place, adding sentences with
        replaced characters as specified in the configuration.

    Raises:
        Exception: If an error occurs during the replacement process.
    """

    for pair in characterReplaceConfig:
        try:
            charIn = pair[0]
            charOut = pair[1]
            totalDatapoints = pair[2]
            characterReplaceTypeToCSV(sentences, charIn, charOut, totalDatapoints)
        except Exception:
            print(f"Error replacing {charIn} by {charOut}.")
            pass

def characterDeleteDatapoints(sentences, characterDeleteConfig):
    """
    This function deletes characters from each sentence in the `sentences` list based on
    the configuration provided in `characterDeleteConfig`.

    Args:
        sentences: A list of strings representing the sentences to process.
        characterDeleteConfig: A list of tuples where each tuple contains:
            - The character to be deleted (charIn).
            - The number of datapoints to generate (totalDatapoints).

    Returns:
        None. The function modifies the `sentences` list in-place, adding sentences with
        deleted characters as specified in the configuration.

    Raises:
        Exception: If an error occurs during the deletion process.
    """

    for pair in characterDeleteConfig:
        try:
            charIn = pair[0]
            totalDatapoints = pair[1]
            characterDeleteTypeToCSV(sentences, charIn, totalDatapoints)
        except Exception:
            print(f"Error deleting {charIn}.")
            pass

def characterAddDatapoints(sentences, characterAddConfig):
    """
    This function adds characters to each sentence in the `sentences` list based on the
    configuration provided in `characterAddConfig`.

    Args:
        sentences: A list of strings representing the sentences to process.
        characterAddConfig: A list of tuples where each tuple contains:
            - The character to be added (charOut).
            - The number of datapoints to generate (totalDatapoints).

    Returns:
        None. The function modifies the `sentences` list in-place, adding sentences with
        added characters as specified in the configuration.

    Raises:
        Exception: If an error occurs during the addition process.
    """

    for pair in characterAddConfig:
        try:
            charOut = pair[0]
            totalDatapoints = pair[1]
            characterAddTypeToCSV(sentences, charOut, totalDatapoints)
        except Exception:
            print(f"Error adding {charOut}.")
            pass

def characterSeqReplaceDatapoints(sentences, characterSeqReplaceConfig):
    """
    This function replaces character sequences in each sentence from the `sentences` list with
    other specified character sequences based on the configuration provided in
    `characterSeqReplaceConfig`.

    Args:
        sentences: A list of strings representing the sentences to process.
        characterSeqReplaceConfig: A list of tuples where each tuple contains:
            - The character sequence to be replaced (charSeqIn).
            - The replacement character sequence (charSeqOut).
            - The number of datapoints to generate (totalDatapoints).

    Returns:
        None. The function modifies the `sentences` list in-place, adding sentences with
        replaced character sequences as specified in the configuration.

    Raises:
        Exception: If an error occurs during the replacement process.
    """

    for pair in characterSeqReplaceConfig:
        try:
            charSeqIn = pair[0]
            charSeqOut = pair[1]
            totalDatapoints = pair[2]
            characterSeqReplaceTypeToCSV(sentences, charSeqIn, charSeqOut, totalDatapoints)
        except Exception:
            print(f"Error replacing characterSeq {charSeqIn} by characterSeq {charSeqOut}.")
            pass

def characterSeqDeleteDatapoints(sentences, characterSeqDeleteConfig):
    """
    This function deletes character sequences from each sentence in the `sentences` list
    based on the configuration provided in `characterSeqDeleteConfig`.

    Args:
        sentences: A list of strings representing the sentences to process.
        characterSeqDeleteConfig: A list of tuples where each tuple contains:
            - The character sequence to be deleted (charSeqIn).
            - The number of datapoints to generate (totalDatapoints).

    Returns:
        None. The function modifies the `sentences` list in-place, adding sentences with
        deleted character sequences as specified in the configuration.

    Raises:
        Exception: If an error occurs during the deletion process.
    """

    for pair in characterSeqDeleteConfig:
        try:
            charSeqIn = pair[0]
            totalDatapoints = pair[1]
            characterSeqDeleteTypeToCSV(sentences, charSeqIn, totalDatapoints)
        except Exception:
            print(f"Error Deleting characterSeq {charSeqIn}.")
            pass

def characterSeqAddDatapoints(sentences, characterSeqAddConfig):
    """
    This function adds character sequences to each sentence in the `sentences` list
    based on the configuration provided in `characterSeqAddConfig`.

    Args:
        sentences: A list of strings representing the sentences to process.
        characterSeqAddConfig: A list of tuples where each tuple contains:
            - The character sequence to be added (charSeqOut).
            - The number of datapoints to generate (totalDatapoints).

    Returns:
        None. The function modifies the `sentences` list in-place, adding sentences with
        the specified character sequences as specified in the configuration.

    Raises:
        Exception: If an error occurs during the addition process.
    """
    for pair in characterSeqAddConfig:
        try:
            charSeqOut = pair[0]
            totalDatapoints = pair[1]
            characterSeqAddToType(sentences, charSeqOut, totalDatapoints)
        except Exception:
            print(f"Error adding characterSeq {charSeqOut}.")
            pass

"""
    Creating single files
"""
def mergeCsvFiles():

    inputFolder="./outputfiles/"
    outputFile="./syntheticData.csv"
    
    # Check if the output folder exists, if not create it
    if not os.path.exists(inputFolder):
        raise FileNotFoundError(f"Input folder '{inputFolder}' does not exist.")

    # Get a list of all CSV files in the input folder
    csvFiles = glob.glob(os.path.join(inputFolder, '*.csv'))

    # Initialize an empty list to store dataframes
    dfs = []

    # Read each CSV file into a DataFrame and append to the list
    for csvFile in csvFiles:
        dfEach = pd.read_csv(csvFile,names=["Correct","Incorrect"])
        dfs.append(dfEach)

    # Concatenate all dataframes into a single dataframe
    mergedDf = pd.concat(dfs, ignore_index=True)

    # Write the merged dataframe to a CSV file
    mergedDf.to_csv(outputFile, index=False)

    # Remove intermediate CSV files
    for csvFile in csvFiles:
        os.remove(csvFile)


