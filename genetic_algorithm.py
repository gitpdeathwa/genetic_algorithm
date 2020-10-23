import random
import math
import pdb

GENE_LEN = 10 # need to be bigger than 1

coordinate_list = {1 : [7, 11], 2 : [3, 6], 3 : [1, 5], 4 : [17, 5], 5: [15, 13],
                    6 : [12, 7], 7 : [5, 4], 8 : [13, 19], 9 : [7, 9], 10 : [18, 17] }
#generate random initial gene 
#start_point need to be key of dict
def GeneInit(gene_num, start_point):
    gene_arr = [None] * gene_num
    for i in range(0, gene_num):
        gene_arr[i] = [None] * GENE_LEN
        gene_arr[i][0] = start_point
        nucleic_arr = list(range(1, GENE_LEN + 1))
        nucleic_arr.remove(start_point)
        for j in range(1, GENE_LEN):
            val = random.randrange(0, len(nucleic_arr))
            gene_arr[i][j] = nucleic_arr[val]
            nucleic_arr.pop(val)

    return gene_arr

def GetDistance(pt1, pt2):
     return round( math.sqrt( ( (pt1[0] - pt2[0]) ** 2 ) + ( (pt1[1] - pt2[1]) ** 2 ) ), 3)

def Fitness(gene):
    dist_total = GetDistance(coordinate_list.get(gene[GENE_LEN-1]), coordinate_list.get(gene[0]))
    for i in range(0, GENE_LEN-1):
        dist_total += GetDistance(coordinate_list.get(gene[i]), coordinate_list.get(gene[i+1]))

    fitness = 10000 / dist_total
    return fitness

def GeneSurvival(gene_arr):
    fitness_table = [None] * len(gene_arr)
    for i in range(len(gene_arr)):
        fitness_table[i] = [None] * 2
        fitness_table[i][0] = gene_arr[i]
        fitness_table[i][1] = Fitness(gene_arr[i])

    sorted_fitness_table = sorted(fitness_table, key = lambda x : x[1], reverse = True)
    return sorted_fitness_table[ 0 : int(len(gene_arr)/ 2)]

def CrossGene(gene_arr): # recommand gene_arr to be sorted by fitnes (by decesending order)
    if (len(gene_arr) % 2) == 1 :
        gene_arr.pop()

    random.shuffle(gene_arr)
    arr1 = gene_arr[ : int(len(gene_arr) / 2)]
    arr2 = gene_arr[int(len(gene_arr) / 2) : ]

    offspring_arr= [None] * int(len(gene_arr) / 2)
    for i in range( int( len(gene_arr) / 2) ):
        offspring_arr[i] = [None] * GENE_LEN

    flag_arr = [1] * int( len(gene_arr) / 2 ) + [0] * int( len(gene_arr) / 2)
    random.shuffle(flag_arr)

    j_tmp = 0

    for i in range( int(len(gene_arr) /2) ):
        for j in range(GENE_LEN) :
            #select according to flag_arr
            if flag_arr[j] == 0:
                offspring_arr[i][j] = arr1[i][j]
            else :
                offspring_arr[i][j] = arr2[i][j]

            #check if  value of current indext is in [ : current_indext ] 
            #if true => switch arr 
            if ( offspring_arr[i][j] in offspring_arr[i][:j] ) == True:
                if flag_arr[j] == 0:
                    offspring_arr[i][j] = arr2[i][j]
                else :
                    offspring_arr[i][j] = arr1[i][j]

                #check if  value of current indext is in [ : current_indext ] 
                # if exist => get index of overlaped part
                if ( offspring_arr[i][j] in offspring_arr[i][:j] ) == True:
                    overlap_index = [x for x in range(0, j) if ( ( arr1[i][x] == arr1[i][j]) or ( arr1[i][x] == arr2[i][j] ) or ( arr2[i][x] == arr1[i][j]) or (arr2[i][x] == arr2[i][j]) )]
                    for z in reversed(range(len(overlap_index))):
                        #if (offspring_arr[i][overlap_index[z]] in offspring_arr[i][:overlap_index[z]] ) == True:
                        #    continue
                        if(flag_arr[overlap_index[z]] == 0):
                            if( arr2[i][overlap_index[z]] in offspring_arr[i][:overlap_index[z]] ) == True:
                                if z == 0 :
                                    del(offspring_arr[i])
                                continue
                            else:
                                offspring_arr[i][overlap_index[z]] = arr2[i][overlap_index[z]]

                        else:
                            if( arr1[i][overlap_index[z]] in offspring_arr[i][:overlap_index[z]] ) == True:
                                if z == 0 :
                                    del(offspring_arr[i])
                                continue
                            else:
                                offspring_arr[i][overlap_index[z]] = arr1[i][overlap_index[z]]
                        #존재하지 않는 다면 염기서열을 상반된 arr리스트의 원소로로 바꾸고 이후 이후 배열은 None으로 초기화
                        offspring_arr[i][overlap_index[z] + 1 : ] =  [None] * len(offspring_arr[i][overlap_index[z] : ])
                        j =  overlap_index[z]
                        break

    return offspring_arr

gene_arr = GeneInit(10, 3)
for i in range( len(gene_arr) ):
    print('[', end = '')
    for j in range( GENE_LEN ):
        print(' %d ' % gene_arr[i][j], end ='')
    print(']', end = '')
    print('       FITNESS : %f ' % Fitness(gene_arr[i]))

print("***** result of survival *****")
survive_gene_arr = GeneSurvival(gene_arr)
for i in range( int( len(gene_arr) / 2)):
    print('[', end = '')
    for j in range( GENE_LEN ):
        print(' %d ' % survive_gene_arr[i][0][j], end ='')
    print(']', end = '')
    print('       FITNESS : %f ' % survive_gene_arr[i][1])


descendant_arr = CrossGene(gene_arr)
for i in range ( len(descendant_arr) ):
    print( '[', end = '')
    for j in range( GENE_LEN ):
        print(" %d " % descendant_arr[i][j], end = '')
    print(']', end = '')

