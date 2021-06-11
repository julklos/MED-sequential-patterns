from SequentialPatternAlgorithm import SequentialPatternAlgorithm
import copy
from Sequence import Sequence
from Pattern import Pattern

class PrefixSpan(SequentialPatternAlgorithm):

    PLACEHOLDER = "_"

    def run(self):
        self._final_sequences = []
        self._prefix_span([], self._data)
        return self._final_sequences


    def _prefix_span(self, alpha, sequencesDb):
        freq = self._frequency_items(alpha, sequencesDb)
        print(freq)
        # for every pattern p in freq
        # p can be assembled to the last element of alpha or can be add as sequential pattern
        for f in freq :  
            print(freq[f])  
            newAlpha = []

            # if _item
            if "_" in f :
                for itemset in alpha :
                    newAlpha.append(itemset)

                #get the last element of alpha    
                newItemset = newAlpha[-1]
                f.replace('_', '')
                newItemset.append(f)
                newItemset.sort()
                # assemble p as the last element of alpha
                newAlpha[-1] = newItemset

            # if item
            else :
                if len(alpha) != 0:
                    for itemset in alpha :
                        newAlpha.append(itemset)
                
                newItemset = [f]
                newAlpha.append(newItemset)

            #TO DO: find the suuport of Patern and take min
            self._final_sequences.append(Pattern(newAlpha, freq[f]))
            projectedDb = []

            for sequence in sequencesDb :
                projectedSequence = self._removeInfrequentElements(sequence, freq)
                suffix = self._getSuffix(projectedSequence, newAlpha[-1])
                if suffix != None and len(suffix.get_itemsets()) != 0 :
                    projectedDb.append(suffix)
            
            if len(projectedDb) != 0 :
                self._prefix_span(newAlpha, projectedDb)

    def _removeInfrequentElements(self, sequence, freq):

        projectedSequence = copy.deepcopy(sequence)
        projectedSequence.delete_infrequent_item_from_itemset(freq)
        return projectedSequence
                

    def _getSuffix(self, sequence, prefix):
        found = False

        for i,itemset in enumerate(sequence.get_itemsets()):
            if self._containAll(prefix,itemset):
                found = True
                break

            else :
                item_tmp = itemset[0].replace('_', '')
                if len(prefix) > 0 and '_' in itemset[0] and prefix[-1] == item_tmp:
                    found = True
                    break

        if found:
            suffix = sequence.get_itemsets()[i:].copy()
            first_suffix = suffix[0].copy()

            if '_' in first_suffix[0] :
                first_suffix.pop(0)
            else :
                to_delete = []
                first_suffix= self._removeAll(first_suffix, prefix)
                for item in first_suffix:
                    if item < prefix[-1]:
                        to_delete.append(item)
                for e in to_delete:
                     first_suffix.remove(e)

            if len(first_suffix) != 0 :
                first_suffix.sort()
                suffix[0] = first_suffix
            else : 
                suffix.pop(0)

            return Sequence(suffix)
            
        else: return None


    def _frequency_items(self, alpha, sequencesDb):

        seqFreq = {}

        #get the last itemset of alpha
        if len(alpha) != 0:
            last_itemset = alpha[-1]
        else:
            last_itemset = []

        for sequence in sequencesDb :

            for itemset in sequence.get_itemsets():
                #see if the itemset contains all items from alpha last itemset
                #if yes then item after the last item of alpha last itemset as _item and item
                if len(last_itemset) != 0 and self._containAll(itemset, last_itemset):
                    
                    # add item in last itemset in alpha
                    for item in last_itemset:
                        if item in seqFreq:
                            seqFreq[item] = seqFreq[item] +1
                        else:
                            seqFreq[item] = 1
                    
                    # add items not included in alpha last itemset
                    leftItemset = self._removeAll(itemset.copy(), last_itemset)
                    for item in leftItemset :
                        if item in seqFreq:
                            seqFreq[item] = seqFreq[item] +1
                        else:
                            seqFreq[item] = 1

                        if "_" + item in seqFreq:
                            seqFreq["_" + item] = seqFreq[item] +1
                        else:
                            seqFreq["_" + item] = 1
                    
                else:
                    for item in itemset:
                        if item in seqFreq:
                            seqFreq[item] = seqFreq[item] +1
                        else:
                            seqFreq[item] = 1

        #remove infrequent items
        newSeqFreq = dict((k,v) for k,v in seqFreq.items() if v > self._min_support)
        return newSeqFreq

    def _containAll(self, list1, list2):

        ifContains = True
        for item in list1:
            if item not in list2:
                ifContains = False
                break
        
        return ifContains

    def _removeAll(self, list1, list2):

        for item in list1:
            if item in list2:
                list1.remove(item)

        return list1