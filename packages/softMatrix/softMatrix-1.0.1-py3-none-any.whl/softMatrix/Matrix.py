from fractions import Fraction

class Matrix:

    def __init__(self, matrix):
        self.matrix=matrix
        self.row=len(matrix)
        self.col=len(matrix[0])
        self.ordre=f"{self.row}x{self.col}"


    """
    méthode show() pour formater l'affichage d'une matrice
    """
    def show(self):
        print("  _")
        for line in range(self.row):
            print(" | ",end="") if line!=self.row-1 else print(" |_",end="")
            for column in range(self.col):
                if(column==self.col-1):
                    if(line==self.row-1):
                        print(f" {self.matrix[line][column]} _|",end="")
                    else: print(f" {self.matrix[line][column]}  |",end="")
                else: print(f" {self.matrix[line][column]} ",end="")
            print()

    """
    méthode identite(ordre) qui renvoit la matrice identite correspondant à l'ordre renseigné
    """
    @staticmethod
    def identite(ordre):
        matrixI=[]
        for line in range(ordre):
            lineI=[]
            for column in range(ordre):
                lineI.append(1 if line==column else 0)
            matrixI.append(lineI)
        return Matrix(matrixI)

    """
    méthode statique same_value(row, col, value) qui retourne une matrice constitué uniquement de la valeur 'value'
    """
    @staticmethod
    def same_value(row, col, value):
        matrixU=[]
        for line in range(row):
            lineU=[]
            for column in range(col):
                lineU.append(value)
            matrixU.append(lineU)
        return Matrix(matrixU)

    """
    méthode statique unite(row, col) qui renvoit la matrice unite au format 'row*col' 
    """
    @staticmethod
    def unite(row, col):
        return Matrix.same_value(row, col, 1)

    """
    méthode statique nulle(row, col) qui renvoit la matrice nulle au format 'row*col' 
    """
    @staticmethod
    def nulle(row, col):
        return Matrix.same_value(row, col, 0)
    

    """
    méthode transpose() permettant d'odtenir la transposée d'une matrice
    """
    def transpose(self):
        matrixT=[]
        for column in range(self.col):
            base=[]
            for line in range(self.row):
                base.append(self.matrix[line][column])
            matrixT.append(base)
        return Matrix(matrixT)


    """
    méthode matrix_mult(coef) qui renvoit une matrice résultant du produit d'une matrice avec un coefficient réel
    """
    def matrix_mult(self, coef):
        matrixMult=[]
        for line in range(self.row):
            lineMult=[]
            for column in range(self.col): lineMult.append(self.matrix[line][column]*coef)
            matrixMult.append(lineMult)
        return Matrix(matrixMult)

    """
    méthode booléenne equal(matrice) qui vérifie l'égalité entre deux matrices
    """
    def equal(self, matrice):
        if(self.ordre!=matrice.ordre): return False
        else:
            for line in range(self.row):
                for column in range(self.col):
                    if(self.matrix[line][column]!=matrice.matrix[line][column]): return False
            return True

    """
    méthode modulo_matrix(modulo) permettant de retourner une matrice dont les éléments sont les modulo des éléments d'une matrice avec un entier
    """
    def modulo_matrix(self, modulo):
        matrixMod=[]
        for i in range(self.row):
            lineMod=[]
            for j in range(self.col):
                lineMod.append(self.matrix[i][j]%modulo)
            matrixMod.append(lineMod)
        return Matrix(matrixMod)


    """
    méthode booléenne norm_somme(*allMatrix) qui permet de vérifier si la somme de 2 matrices ou plus est possible
    """
    def norm_somme(self, *allMatrix, fromS=False):
        if fromS:allMatrix=allMatrix[0]
        for matrice in allMatrix:
            if self.row!=matrice.row or self.col!=matrice.col:
                return False
        return True

    """
    méthode somme_matrix(*allMatrix) qui renvoit la somme de 2 matrices ou plus si norm_somme(*allMatrix) est vrai et renvoit un 'NoneType' dans le cas contraire
    """
    def somme_matrix(self, *allMatrix):
        if(self.norm_somme(allMatrix, fromS=True)):
            matrixS=self
            for matrice in allMatrix:
                base=[]
                for line in range(matrixS.row):
                    lineS=[]
                    for column in range(matrixS.col):
                        lineS.append(matrixS.matrix[line][column]+(matrice.matrix[line][column]))
                    base.append(lineS)
                matrixS=Matrix(base)
            return matrixS
        else: return None

    """
    méthode diff_matrix(matrice) renvoyant la différence entre 2 matrices (elle utilise la somme_matrix(*allMatrix) pour appliquer le même principe mais en multipliant d'abord -1 à la 2e matrice grâce à matrix_mult(coef))
    """
    def diff_matrix(self, matrice):
        return self.somme_matrix(matrice.matrix_mult(-1))


    """
    méthode booléenne norm_produit(*allMatrix) permettant de vérifier si 2 matrices ou plus respectent les conditions necessiares pour effectuer un produit entre elles
    """
    def norm_produit(self, *allMatrix, fromP=False):
        if fromP:allMatrix=allMatrix[0]
        prevM=self
        for nextM in allMatrix:
            if prevM.col!=nextM.row:
                return False
            prevM=nextM
        return True

    """
    méthode produit_matrix(*allMatrix) qui permet de rnevoyer le produit de 2 matrices ou plus si norm_produit(*allMatrix) est vrai et renvoit un 'NoneType' dans le cas contraire 
    """
    def produit_matrix(self, *allMatrix):
        if(self.norm_produit(allMatrix, fromP=True)):
            matriceP=self
            for matrice in allMatrix:
                base=[]
                for i in range(matriceP.row):
                    lineP=[]
                    for j in range(matrice.col):
                        element=0
                        for k in range(matrice.row):
                            element+=(matriceP.matrix[i][k]*matrice.matrix[k][j])
                        lineP.append(element)
                    base.append(lineP)
                matriceP=Matrix(base)
            return matriceP
        else: return None

    """
    méthode booléenne matrix_carre() permettant de vérifier si une matrice est carrée
    """
    def matrix_carre(self):
        return self.row==self.col

    """
    méthode booléenne is_inverse(matrice) qui vérifie si une matrice est l'inverse d'une autre 'matrice'
    """
    def is_inverse(self, matrice):
        if(not self.matrix_carre() or self.ordre!=matrice.ordre): return False
        else:
            return self.produit_matrix(matrice).equal(Matrix.identite(self.row))


    """
    méthode extract_matrix(interRow, interCol) permettant d'extraire une matrice associé à un coefficient  de la matrice en renseignant la ligne(interRow) et la colonne(interCol) du coefficient, si l'un de ces paramètres est invalide (ligne ou colonne inexistante danns la matrice), ça sera un 'NoneType' qui sera renvoyé
    """
    def extract_matrix(self, interRow, interCol):
        if(interRow<self.row and interCol<self.col):
            matrixE=[]
            for line in range(self.row):
                lineE=[]
                for column in range(self.col):
                    if(line!=interRow and column!=interCol):
                        lineE.append(self.matrix[line][column])
                if lineE: matrixE.append(lineE)
            return Matrix(matrixE)
        else: return None

    """
    méthode statique sumTab(tab) qui permet de renvoyer la somme des éléments d'un tableau unidimensionnel (vecteur)
    """
    @staticmethod
    def sumTab(tab):
        sum=0
        for element in tab: sum+=element
        return sum

    """
    méthode récursive determinant() qui calcule et renvoit le déterminant d'une matrice lorqu'elle est carrée sinon un 'NoneType' est retourné
    """
    def determinant(self):
        if(self.matrix_carre()):
            minMatrix=self
            if(minMatrix.ordre=="1x1"): return minMatrix.matrix[0][0]
            else:
                valuesDet, signe=[], 1
                for column in range(minMatrix.col):
                    valuesDet.append(signe*minMatrix.matrix[0][column]*self.extract_matrix(0, column).determinant())
                    signe*=-1
                return Matrix.sumTab(valuesDet)
        else: return None

    """
    méthode booléenne inversible() vérifiant si une matrice est inversible
    """
    def inversible(self):
        return self.matrix_carre() and self.determinant()!=0

    """
    méthode matrix_signe(row, col) permettant d'afficher les signes correspondants aux éléments d'une matrice d'ordre donné (row*col)
    """
    @staticmethod
    def matrix_signe(row, col):
        for line in range(row):
            for column in range(col):
                signe=(-1)**(line+column)
                print(" | +" if signe==1 else " | -",end="")
            print()


    """
    méthode mineur(line, column) qui renvoit le mineur associé à un élément d'une matrice de position (line,column) si cette dernière est valide, dans le cas contraire un 'NoneType' est renvoyé
    """
    def mineur(self, line, column):
        if(self.matrix_carre()):
            return self.extract_matrix(line, column).determinant()
        else: return None

    """
    méthode cofacteur(line, column) qui renvoit le cofacteur associé à un élément d'une matrice de position (line,column); il s'agit d'un réel résultant du mineur associé au signe dans la matrice des signes. Un 'NoneType' est renvoyé si la position (line,column) est incorrecte
    """
    def cofacteur(self, line, column):
        if(self.matrix_carre()):
            signe=(-1)**(line+column)
            return signe*self.mineur(line, column)
        else: return None

    """
    méthode comatrice() renvoyant la comatrice d'une matrice; il s'agit de la matrice des cofacteurs
    """
    def comatrice(self):
        com=[]
        for line in range(self.row):
            lineC=[]
            for column in range(self.col):
                lineC.append(self.cofacteur(line, column))
            com.append(lineC)
        return Matrix(com)


    """
    méthode matrix_inverse() permettant de retourner l'inverse d'une matrice dans la mesure du possible sinon un 'NoneType' est retourné
    """
    def matrix_inverse(self):
        if self.inversible():
            return self.comatrice().transpose().matrix_mult(Fraction(1,self.determinant()))
        else: return None