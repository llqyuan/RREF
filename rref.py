# The purpose of this program is to row reduce a matrix to its
#   reduced row echelon form (RREF).

# A Matrix is a nonempty (listof (listof (anyof Int Float))) where each
#   sublist is nonempty and of the same length.


# =====================================================
# Row operations and minor helpers


def print_matrix(M,end=""):
    '''
    Prints the matrix M, as well as the string end.

    Effects: Prints to the screen

    print_matrix: Matrix Str-> None
    '''
    num_rows = len(M)
    if num_rows!=0:
        num_cols=len(M[0])

    i = 0
    s="\n"

    while i < num_rows:

        j=0

        while j < num_cols:

            s = s + "{1}{0}".format(M[i][j],
                                    " "*(max(1,(8-len(str(M[i][j]))))))
            j = j+1
            
        if i<num_rows-1:
            s = s + "\n"
            
        i = i+1

    s += end
    print(s)


def int_or_round(n):
    '''
    Returns n as an integer if it is "close" to an integer, and returns
    n otherwise. That is: If for some integer i, abs(n-i) < 0.0001,
    returns i. Otherwise, returns n rounded to the nearest 4 decimals.

    int_or_round: (anyof Int Float) -> (anyof Float Int)
    '''
    if abs(n-int(n)) < 0.0001:
        n = int(n)
    elif abs(n-int(n+1)) < 0.0001:
        n = int(n+1)
    elif abs(n-int(n-1)) < 0.0001:
        n = int(n-1)
    
    else:
        temp = n*10000
        calc = int(temp*10)
        if calc>=0 and calc%10 < 5: # Non-negative and last digit <5
            temp = int(temp)
            n = temp/10000
        elif abs(calc)%10 < 5: # Negative and last digit <5
            temp = int(temp)
            n = temp/10000
        elif calc>=0: # Non-negative and last digit >=5
            temp = int(temp+1)
            n = temp/10000
        else: # Negative and last digit >=5
            temp = int(temp-1)
            n = temp/10000
    
    return n


def mult_row(M, row_i, c):
    '''
    Performs the row operation c*(R_{row_i}) on M (multiplying the
    row_i-th row by a real number c)

    Effects: Mutates M

    mult_row: Matrix Nat (anyof Int Float) -> None
    '''
    col = 0

    while col<len(M[row_i]):
        M[row_i][col] = int_or_round(c*M[row_i][col])
        col = col+1


def add_row(M, add_to, added, c):
    '''
    Performs the row operation R_{add_to} + c*(R_{added}) on M (adding
    a multiple of the added-th row to the add_to-th row).

    Effects: Mutates M

    add_row: Matrix Nat Nat (anyof Int Float) -> None
    '''
    col = 0

    while col<len(M[add_to]):
        M[add_to][col] = int_or_round(M[add_to][col] + c*M[added][col])
        col = col+1

def swap_row(M, i, j):
    '''
    Performs the row operation R_i <-> R_j on M (swapping the ith row with
    the jth row)

    Effects: Mutates M

    swap_row: Matrix Nat Nat -> None
    '''
    row_i = M[i]
    row_j = M[j]
    M[i] = row_j
    M[j] = row_i


# =====================================================
# Row reducing


def reduce_column(M, col, start_from_row):
    '''
    Performs necessary row operations on M to get a leading one
    into the row start_from_row in the col-th column, if possible,
    noting that all rows above start_from_row have a leading one in
    them. If it is not possible, returns a message indicating that
    there are only zero entries in the column.

    Effects: Mutates M

    reduce_column: Matrix Nat Nat -> (anyof None "column is all zeroes")
    '''

    # Find the first nonzero entry, if any
    
    f_nonz_i = start_from_row
    
    while f_nonz_i<len(M) and M[f_nonz_i][col]==0: 
        f_nonz_i = f_nonz_i + 1
    
    if f_nonz_i>=len(M): # No nonzero entries
        return "column is all zeroes"


    # Convert into a leading one
    
    row_mult_factor = 1/M[f_nonz_i][col]
    mult_row(M, f_nonz_i, row_mult_factor)


    # Row-reduce to have the leading one be the only nonzero entry in column
    
    i = f_nonz_i + 1
    j = f_nonz_i - 1
    
    while i<len(M):

        if M[i][col]!=0:
            add_factor = -M[i][col]
            add_row(M, i, f_nonz_i, add_factor)
            
        i = i+1

    while j>=0:

        if M[j][col]!=0:
            add_factor = -M[j][col]
            add_row(M,j,f_nonz_i,add_factor)

        j = j-1


    # Move leading one to the top

    swap_row(M,start_from_row,f_nonz_i)


def reduce(M):
    '''
    Reduces M to row reduced echelon form, and prints the result.

    Effects:

    Mutates M
    Prints to the screen

    reduce: Matrix -> None
    '''
    print_matrix(M,end="      Starting matrix")
    
    col = 0
    start_from_row = 0
    
    # start_from_row tracks which row to put the leading one in.
    #   As well, the rows above it have already been reduced
    #   (ie. the leading ones are in the proper locations)

    
    while start_from_row < len(M) and col < len(M[0]):

        print_matrix(M, end="      ~")
        
        flag = reduce_column(M,col,start_from_row)
        col = col+1
        
        if flag!="column is all zeroes":
            start_from_row += 1

    print_matrix(M, end="      RREF\n")

'''
# Tests

reduce([[0,0],[0,1]])

reduce([[1,0],[0,1]]) # Identity matrix
reduce([[0,0],[0,0]]) # Zero matrix
reduce([[0,1],[0,0]]) # RREF, not invertible, free variable 1st column
reduce([[1,0],[0,0]]) # RREF, not invertible, free variable 2nd column
reduce([[0,0],[1,0]]) # Switch rows
reduce([[2,0],[0,0]]) # Multiply by nonzero scalar
reduce([[1,-4],[0,1]]) # Add a multiple of one row to another

reduce([[2,3,0],[1,1,0]]) # 3rd column zero
reduce([[0,0,1],[2,0,3]]) # 2nd column zero
reduce([[0,2,4],[0,1,0]]) # 1st column zero

reduce([[2,3,4],[1,2,1],[5,2,0]]) # typical invertible
reduce([[1,4,3,2],[2,3,1,1]]) # noninvertible (leading ones in 1,2)
reduce([[1,0,3,2],[2,0,1,1]]) # noninvertible (1,3)
reduce([[1,0,0,2],[1,0,0,4]]) # noninvertible (1,4)
reduce([[0,1,2,3],[0,2,3,2]]) # noninvertible (2,3)
reduce([[2,4,4,2],[3,6,6,3],[0,0,2,0]]) # noninvertible (1,3) with zero row
reduce([[1,2,3,4],[0,0,2,0],[0,0,0,0]]) # noninvertible with zero row


reduce([[2,3],[2,4],[1,1],[2,1]]) # more rows than columns
'''

# Sample
reduce([[2,4,4,2],[3,6,6,3],[0,0,2,0]])
