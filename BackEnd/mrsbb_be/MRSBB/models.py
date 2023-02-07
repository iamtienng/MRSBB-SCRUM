from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager as AbstractUserManager
import numpy as np
from MRSBB.mfcf import MatrixFactorization
# Create your models here.


class UserAccountManager(AbstractUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True

        user.set_password(password)
        user.save()

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    gender = models.CharField(max_length=30, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    objects = UserAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'gender', 'birth_date']

    def get_full_name(self):
        return self.first_name + self.last_name

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.email

    def create_wt_d_for_user(self):
        new_Wt = WTModels(id=self.id, e1=0.0, e2=0.0, e3=0.0, e4=0.0, e5=0.0, e6=0.0, e7=0.0, e8=0.0, e9=0.0, e10=0.0, e11=0.0, e12=0.0, e13=0.0, e14=0.0, e15=0.0, e16=0.0, e17=0.0, e18=0.0, e19=0.0, e20=0.0, e21=0.0, e22=0.0, e23=0.0, e24=0.0, e25=0.0,
                          e26=0.0, e27=0.0, e28=0.0, e29=0.0, e30=0.0, e31=0.0, e32=0.0, e33=0.0, e34=0.0, e35=0.0, e36=0.0, e37=0.0, e38=0.0, e39=0.0, e40=0.0, e41=0.0, e42=0.0, e43=0.0, e44=0.0, e45=0.0, e46=0.0, e47=0.0, e48=0.0, e49=0.0, e50=0.0)
        new_Wt.save()
        new_d = dModels(id=self.id, e1=0.0)
        new_d.save()

    def train_wt_d_for_user(self):
        userID = self.id
        ratingObjs = Rating.objects.all()
        ratings_matrix = np.asmatrix(
            ratingObjs.values_list('userId', 'movieId', 'rating'))
        XObjs = XModels.objects.all()
        X = np.asarray(XObjs.values_list('e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16', 'e17', 'e18', 'e19', 'e20', 'e21', 'e22', 'e23', 'e24',
                                         'e25', 'e26', 'e27', 'e28', 'e29', 'e30', 'e31', 'e32', 'e33', 'e34', 'e35', 'e36', 'e37', 'e38', 'e39', 'e40', 'e41', 'e42', 'e43', 'e44', 'e45', 'e46', 'e47', 'e48', 'e49', 'e50'))
        WTobjs = WTModels.objects.all()
        WT = np.asarray(WTobjs.values_list('e1', 'e2', 'e3', 'e4', 'e5', 'e6', 'e7', 'e8', 'e9', 'e10', 'e11', 'e12', 'e13', 'e14', 'e15', 'e16', 'e17', 'e18', 'e19', 'e20', 'e21', 'e22', 'e23',
                                           'e24', 'e25', 'e26', 'e27', 'e28', 'e29', 'e30', 'e31', 'e32', 'e33', 'e34', 'e35', 'e36', 'e37', 'e38', 'e39', 'e40', 'e41', 'e42', 'e43', 'e44', 'e45', 'e46', 'e47', 'e48', 'e49', 'e50'))
        W = WT.T
        bObjs = bModels.objects.all()
        b = np.asarray(bObjs.values_list('e1'))
        dObjs = dModels.objects.all()
        d = np.asarray(dObjs.values_list('e1'))

        mfcf_model = MatrixFactorization(Y=ratings_matrix, K=50, lam=.01, Xinit=X,
                                         Winit=W, bInit=b, dInit=d, learning_rate=50)
        mfcf_model.b = mfcf_model.b.reshape(mfcf_model.b.shape[0], )
        mfcf_model.d = mfcf_model.d.reshape(mfcf_model.d.shape[0], )
        mfcf_model.updateWdUserU(userID)

        # update Bias d for user userID
        dUser = dModels.objects.get(id=userID)
        dUser.e1 = mfcf_model.d[userID]
        dUser.save()

        # update W-Transpose for user userID
        WtUser = WTModels.objects.get(id=userID)
        WtUser.e1 = mfcf_model.W[0, userID]
        WtUser.e2 = mfcf_model.W[1, userID]
        WtUser.e3 = mfcf_model.W[2, userID]
        WtUser.e4 = mfcf_model.W[3, userID]
        WtUser.e5 = mfcf_model.W[4, userID]
        WtUser.e6 = mfcf_model.W[5, userID]
        WtUser.e7 = mfcf_model.W[6, userID]
        WtUser.e8 = mfcf_model.W[7, userID]
        WtUser.e9 = mfcf_model.W[8, userID]
        WtUser.e10 = mfcf_model.W[9, userID]
        WtUser.e11 = mfcf_model.W[10, userID]
        WtUser.e12 = mfcf_model.W[11, userID]
        WtUser.e13 = mfcf_model.W[12, userID]
        WtUser.e14 = mfcf_model.W[13, userID]
        WtUser.e15 = mfcf_model.W[14, userID]
        WtUser.e16 = mfcf_model.W[15, userID]
        WtUser.e17 = mfcf_model.W[16, userID]
        WtUser.e18 = mfcf_model.W[17, userID]
        WtUser.e19 = mfcf_model.W[18, userID]
        WtUser.e20 = mfcf_model.W[19, userID]
        WtUser.e21 = mfcf_model.W[20, userID]
        WtUser.e22 = mfcf_model.W[21, userID]
        WtUser.e23 = mfcf_model.W[22, userID]
        WtUser.e24 = mfcf_model.W[23, userID]
        WtUser.e25 = mfcf_model.W[24, userID]
        WtUser.e26 = mfcf_model.W[25, userID]
        WtUser.e27 = mfcf_model.W[26, userID]
        WtUser.e28 = mfcf_model.W[27, userID]
        WtUser.e29 = mfcf_model.W[28, userID]
        WtUser.e30 = mfcf_model.W[29, userID]
        WtUser.e31 = mfcf_model.W[30, userID]
        WtUser.e32 = mfcf_model.W[31, userID]
        WtUser.e33 = mfcf_model.W[32, userID]
        WtUser.e34 = mfcf_model.W[33, userID]
        WtUser.e35 = mfcf_model.W[34, userID]
        WtUser.e36 = mfcf_model.W[35, userID]
        WtUser.e37 = mfcf_model.W[36, userID]
        WtUser.e38 = mfcf_model.W[37, userID]
        WtUser.e39 = mfcf_model.W[38, userID]
        WtUser.e40 = mfcf_model.W[39, userID]
        WtUser.e41 = mfcf_model.W[40, userID]
        WtUser.e42 = mfcf_model.W[41, userID]
        WtUser.e43 = mfcf_model.W[42, userID]
        WtUser.e44 = mfcf_model.W[43, userID]
        WtUser.e45 = mfcf_model.W[44, userID]
        WtUser.e46 = mfcf_model.W[45, userID]
        WtUser.e47 = mfcf_model.W[46, userID]
        WtUser.e48 = mfcf_model.W[47, userID]
        WtUser.e49 = mfcf_model.W[48, userID]
        WtUser.e50 = mfcf_model.W[49, userID]
        WtUser.save()


class Rating(models.Model):
    userId = models.IntegerField()
    movieId = models.IntegerField()
    rating = models.IntegerField()
    timestamp = models.DateTimeField(auto_now=True)


class Movie(models.Model):
    movieId = models.IntegerField()
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    posterUrl = models.CharField(max_length=255)


class XModels(models.Model):
    e1 = models.FloatField()
    e2 = models.FloatField()
    e3 = models.FloatField()
    e4 = models.FloatField()
    e5 = models.FloatField()
    e6 = models.FloatField()
    e7 = models.FloatField()
    e8 = models.FloatField()
    e9 = models.FloatField()
    e10 = models.FloatField()
    e11 = models.FloatField()
    e12 = models.FloatField()
    e13 = models.FloatField()
    e14 = models.FloatField()
    e15 = models.FloatField()
    e16 = models.FloatField()
    e17 = models.FloatField()
    e18 = models.FloatField()
    e19 = models.FloatField()
    e20 = models.FloatField()
    e21 = models.FloatField()
    e22 = models.FloatField()
    e23 = models.FloatField()
    e24 = models.FloatField()
    e25 = models.FloatField()
    e26 = models.FloatField()
    e27 = models.FloatField()
    e28 = models.FloatField()
    e29 = models.FloatField()
    e30 = models.FloatField()
    e31 = models.FloatField()
    e32 = models.FloatField()
    e33 = models.FloatField()
    e34 = models.FloatField()
    e35 = models.FloatField()
    e36 = models.FloatField()
    e37 = models.FloatField()
    e38 = models.FloatField()
    e39 = models.FloatField()
    e40 = models.FloatField()
    e41 = models.FloatField()
    e42 = models.FloatField()
    e43 = models.FloatField()
    e44 = models.FloatField()
    e45 = models.FloatField()
    e46 = models.FloatField()
    e47 = models.FloatField()
    e48 = models.FloatField()
    e49 = models.FloatField()
    e50 = models.FloatField()


class WTModels(models.Model):
    e1 = models.FloatField()
    e2 = models.FloatField()
    e3 = models.FloatField()
    e4 = models.FloatField()
    e5 = models.FloatField()
    e6 = models.FloatField()
    e7 = models.FloatField()
    e8 = models.FloatField()
    e9 = models.FloatField()
    e10 = models.FloatField()
    e11 = models.FloatField()
    e12 = models.FloatField()
    e13 = models.FloatField()
    e14 = models.FloatField()
    e15 = models.FloatField()
    e16 = models.FloatField()
    e17 = models.FloatField()
    e18 = models.FloatField()
    e19 = models.FloatField()
    e20 = models.FloatField()
    e21 = models.FloatField()
    e22 = models.FloatField()
    e23 = models.FloatField()
    e24 = models.FloatField()
    e25 = models.FloatField()
    e26 = models.FloatField()
    e27 = models.FloatField()
    e28 = models.FloatField()
    e29 = models.FloatField()
    e30 = models.FloatField()
    e31 = models.FloatField()
    e32 = models.FloatField()
    e33 = models.FloatField()
    e34 = models.FloatField()
    e35 = models.FloatField()
    e36 = models.FloatField()
    e37 = models.FloatField()
    e38 = models.FloatField()
    e39 = models.FloatField()
    e40 = models.FloatField()
    e41 = models.FloatField()
    e42 = models.FloatField()
    e43 = models.FloatField()
    e44 = models.FloatField()
    e45 = models.FloatField()
    e46 = models.FloatField()
    e47 = models.FloatField()
    e48 = models.FloatField()
    e49 = models.FloatField()
    e50 = models.FloatField()


class bModels(models.Model):
    e1 = models.FloatField()


class dModels(models.Model):
    e1 = models.FloatField()
