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
        nucleic_arr = list(range(1, len(coordinate_list) + 1))
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
    #fitness_ tabel define
    fitness_table = [[0] * 2 for i in range( len(gene_arr) )]
    for i in range( len(gene_arr) ):
        fitness_table[i][0] = i
        fitness_table[i][1] = Fitness(gene_arr[i])

    fitness_table = sorted(fitness_table, key = lambda x : x[1], reverse = True)

    survived_gene_arr = [None] *  len(gene_arr)
    for i in range( len(gene_arr) ):
        survived_gene_arr[i] = gene_arr[fitness_table[i][0]]

    return survived_gene_arr

    #return
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

    flag_arr =  [[1] * int( GENE_LEN / 2 ) + [0] * int( GENE_LEN / 2) for i in range( int(len(gene_arr) /2 ))]
    for i in range( int(len(gene_arr) / 2 ) ):
        random.shuffle(flag_arr[i])

    for i in range( int(len(gene_arr) /2) ):
        j = 0 # for while
        conflicted_index_arr = []
        while True:
            if GENE_LEN == j :
                break
            if flag_arr[i][j] == 0:
                offspring_arr[i][j] = arr1[i][j]
            else :
                offspring_arr[i][j] = arr2[i][j]

            # if same value at backward of offspring_list then alter either arr1 => arr2 or arr2 => arr1
            if ( offspring_arr[i][j] in offspring_arr[i][:j] ) == True:
                if flag_arr[i][j] == 0:
                    offspring_arr[i][j] = arr2[i][j]
                    flag_arr[i][j] = 1
                else :
                    offspring_arr[i][j] = arr1[i][j]
                    flag_arr[i][j] = 0

                # if above process didn't work than modify backward index that overlap value with value of current index 
                if ( offspring_arr[i][j] in offspring_arr[i][:j] ) == True :    
                    if j in conflicted_index_arr :
                        offspring_arr[i] = None
                        break
                    conflicted_index_arr.append(j)
                    overlap_index = [x for x in range(0, j) if ( ( arr1[i][x] == arr1[i][j]) or ( arr1[i][x] == arr2[i][j] ) or ( arr2[i][x] == arr1[i][j]) or (arr2[i][x] == arr2[i][j]) )]
                    for z in reversed(range(len(overlap_index))):
                        if flag_arr[i][overlap_index[z]] == 0 :
                            if( arr2[i][overlap_index[z]] in offspring_arr[i][:overlap_index[z]] ) == True:
                                if z == 0 :
                                    offspring_arr[i] = None
                                    j = GENE_LEN - 1
                                continue
                            else:
                                offspring_arr[i][overlap_index[z]] = arr2[i][overlap_index[z]]

                        else:
                            if( arr1[i][overlap_index[z]] in offspring_arr[i][:overlap_index[z]] ) == True:
                                if z == 0 :
                                    offspring_arr[i] = None
                                    j = GENE_LEN - 1
                                continue
                            else:
                                offspring_arr[i][overlap_index[z]] = arr1[i][overlap_index[z]]
                        #존재하지 않는 다면 염기서열을 상반된 arr리스트의 원소로로 바꾸고 이후 이후 배열은 None으로 초기화
                        offspring_arr[i][overlap_index[z] + 1 : ] =  [None] * len(offspring_arr[i][overlap_index[z] + 1 : ])
                        j =  overlap_index[z]
                        flag_1 = True
                        break
            j += 1
    count = 0
    while count < len(offspring_arr):
        if offspring_arr[count] == None:
            del(offspring_arr[count])
        else:
            count += 1

    return offspring_arr

def Print2DGeneArr(arr, width):
    if arr == None:
        return

    fitness_total = 0
    fitness_num= 0
    for i in range( len(arr) ):

        if arr[i] == None :
            print("[ None ]")
            continue

        print('[', end = '')
        for j in range( width ):
            if arr [i][j] == None:
                #print(" None ", end = '')
                continue

            print(" %d " % arr[i][j], end = '')
        print("]", end ='')
        fitness = Fitness(arr[i])
        fitness_total += fitness
        fitness_num+= 1
        print('       FITNESS : %f ' % fitness )

    print("** FITNESS AVERAGE : %.3f **" % (fitness_total / fitness_num))

def GetGeneArrFitAver(gene_arr):
    fit_total = 0
    fit_num = 0
    for i in range( len(gene_arr) ):
        if gene_arr[i] == None :
            continue

        fit_total += Fitness(gene_arr[i])
        fit_num += 1

    return fit_total / fit_num



#main process
gene_arr = GeneInit(100000, 3)
#Print2DGeneArr(gene_arr, GENE_LEN)

print("inital gene fitness average : %.3f" % GetGeneArrFitAver(gene_arr))

for i in range(20):
    survived_gene_arr = GeneSurvival(gene_arr)
    gene_arr = ( CrossGene(survived_gene_arr) + CrossGene(survived_gene_arr) )
    print("****#%d gene fitness average : %.3f and len(gene_arr) : %d****" % (i, GetGeneArrFitAver(gene_arr), len(gene_arr)) )
    #Print2DGeneArr(gene_arr, GENE_LEN)



