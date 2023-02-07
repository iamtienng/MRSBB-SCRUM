import numpy as np


class MatrixFactorization(object):
    def __init__(self, Y, K, lam=0.1, Xinit=None, Winit=None, bInit=None, dInit=None,
                 learning_rate=0.5):
        self.Y = Y      # represents the utility matrix
        self.K = K      # number of features
        self.lam = lam  # regularization parameter
        self.learning_rate = learning_rate  # for gradient descent
        self.n_users = int(np.max(Y[:, 0])) + 1
        self.users_ids = np.unique(np.asarray(
            Y[:, 0].reshape(Y[:, 0].shape[0]))).astype(np.int32)
        self.n_items = int(np.max(Y[:, 1])) + 1
        self.items_ids = np.unique(np.asarray(
            Y[:, 1].reshape(Y[:, 1].shape[0]))).astype(np.int32)
        self.n_ratings = Y.shape[0]
        self.X = np.random.randn(self.n_items, K) if Xinit is None else Xinit
        self.W = np.random.randn(K, self.n_users) if Winit is None else Winit
        self.b = np.random.randn(self.n_items) if bInit is None else bInit
        self.d = np.random.randn(self.n_users) if dInit is None else dInit

    def updateXb(self):
        for m in self.items_ids:
            ids = np.where(self.Y[:, 1] == m)[0]  # row indices of items m
            user_ids, ratings = self.Y[ids, 0].astype(np.int32), self.Y[ids, 2]
            Wm, dm = self.W[:, user_ids], self.d[user_ids]
            Wm = Wm.reshape(Wm.shape[0], Wm.shape[1])
            for i in range(30):  # 30 iteration for each sub problem
                xm = self.X[m]
                error = Wm.T.dot(xm).reshape(-1, 1) + self.b[m] + dm - ratings
                grad_xm = Wm.dot(error)/self.n_ratings + \
                    (self.lam*xm).reshape(-1, 1)
                grad_bm = np.sum(error)/self.n_ratings
                # gradient descent
                self.X[m] -= np.array((self.learning_rate*grad_xm).T)[0]
                self.b[m] -= self.learning_rate*grad_bm

    def updateWd(self):
        for n in self.users_ids:
            # get all items rated by user n, and the corresponding ratings
            ids = np.where(self.Y[:, 0] == n)[0]
            item_ids, ratings = self.Y[ids, 1].astype(np.int32), self.Y[ids, 2]
            Xn, bn = self.X[item_ids], self.b[item_ids]
            for i in range(30):  # 30 iteration for each sub problem
                wn = self.W[:, n]
                error = Xn.dot(wn) + bn + self.d[n] - ratings
                grad_wn = Xn.T.dot(error)/self.n_ratings + self.lam*wn
                grad_dn = np.sum(error)/self.n_ratings
                # gradient descent
                self.W[:, n] -= np.array(self.learning_rate *
                                         grad_wn.reshape(-1))[0]
                self.d[n] -= self.learning_rate*grad_dn

    def updateXbItemI(self, itemID):
        m = itemID
        ids = np.where(self.Y[:, 1] == m)[0]  # row indices of items m
        user_ids, ratings = self.Y[ids, 0].astype(np.int32), self.Y[ids, 2]
        Wm, dm = self.W[:, user_ids], self.d[user_ids]
        Wm = Wm.reshape(Wm.shape[0], Wm.shape[1])
        for i in range(30):  # 30 iteration for each sub problem
            xm = self.X[m]
            error = Wm.T.dot(xm).reshape(-1, 1) + self.b[m] + dm - ratings
            grad_xm = Wm.dot(error)/self.n_ratings + \
                (self.lam*xm).reshape(-1, 1)
            grad_bm = np.sum(error)/self.n_ratings
            # gradient descent
            self.X[m] -= np.array((self.learning_rate*grad_xm).T)[0]
            self.b[m] -= self.learning_rate*grad_bm

    def updateWdUserU(self, userID):
        n = userID
        # get all items rated by user n, and the corresponding ratings
        ids = np.where(self.Y[:, 0] == n)[0]
        item_ids, ratings = self.Y[ids, 1].astype(np.int32), self.Y[ids, 2]
        Xn, bn = self.X[item_ids], self.b[item_ids]
        for i in range(30):  # 30 iteration for each sub problem
            wn = self.W[:, n]
            error = Xn.dot(wn) + bn + self.d[n] - ratings
            grad_wn = Xn.T.dot(error)/self.n_ratings + self.lam*wn
            grad_dn = np.sum(error)/self.n_ratings
            # gradient descent
            self.W[:, n] -= np.array(self.learning_rate*grad_wn.reshape(-1))[0]
            self.d[n] -= self.learning_rate*grad_dn

    def fit(self):
        for it in range(self.max_iter):
            self.updateXb()
            self.updateWd()

    def pred(self, u, i):
        # predict the rating of user u for item i
        u, i = int(u), int(i)
        try:
            pred = self.X[i, :].dot(self.W[:, u]) + self.b[i] + self.d[u]
        except:
            return 0
        return max(0, min(5, pred))

    def predTopTen(self, u):
        user_id = u
        # predict the top 10 items for user user_id
        items_ids = np.unique(np.asarray(self.Y[:, 1].reshape(
            self.Y[:, 1].shape[0]))).astype(np.int32)
        ids = np.where(self.Y[:, 0] == user_id)[0]
        rated_item_ids = self.Y[ids, 1].astype(np.int32)
        unrated_item_ids = [x for x in items_ids if x not in rated_item_ids]
        items_ids = unrated_item_ids
        predForUserU = np.random.randn(len(items_ids), 2)
        for i in range(len(items_ids)):
            predForUserU[i] = [items_ids[i], self.pred(u=user_id, i=i)]
        predForUserU = predForUserU[predForUserU[:, 1].argsort()][::-1]
        idsTopTen = predForUserU[:10, 0].astype(np.int32).tolist()
        ratingsTopTen = predForUserU[:10, 1].tolist()
        return(idsTopTen, ratingsTopTen)
