/**********
This program is used to convert CG conf. to All-Atom structure
  -developed by Ya-Zhou Shi,Xun-Xun Wang, Li-Zhou, Ya-Lan Tan based on the rmsd1.0.c from Xi Zhang:
***********/
#include<stdio.h>
#include<math.h>
#include<dirent.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<time.h>
#include<string.h>
#include<stdlib.h>
#define     w   0.02         //生成R矩阵时乘上这个系数是为了防止因矩阵元过大而导致特征值难以计算
#define  RMSD_limit 3.0      //RMSD上限，如果片段与CG核苷酸RMSD大于该值，则无法匹配；
#define cut 1.60
#define nm_frag 8
FILE *fragA[20],*fragG[20],*fragC[20],*fragU[20],*CG,*out_AA;
FILE *inpdb, *outpdb;
char atom[20][5000],typen_A[20][50][4],typen_G[20][50][4],typen_C[20][50][4],typen_U[20][50][4],type[5000][4],typen_AA[20][5000][4];
char type_A[20][50][5],type_G[20][50][5],type_C[20][50][5],type_U[20][50][5],type_AA[20][5000][5];
float x_A[20][5][50],x_G[20][5][50],x_C[20][5][50],x_U[20][5][50],x[5][5000];
int id[20],idnu[20],duo1,duo2,NA[20],NG[20],NC[20],NU[20],N,N_AA[20],nucl_AA,atom_AA[20][5000];
char mark1,mark2,mark3,chain[20];
float r,Q,f;
float x_CG[20][5][5],y_CG[5][5],R[5][5],R_T[5][5], xmiddle[20][5],ymiddle[5];
double eigenvalue[5], lambda, Tao[5][5], A[5][5], U[20][5][5], B[5][5], dis, dis_r;
float x_AA[20][5][50],xy[5];
char atomCG[5000][5],typeACG[5000][5],chainCG[5000][5];
int idCG[5000],idnuCG[5000];
char QatomCG[5000][5],QtypeACG[5000][5],QchainCG[5000][5],Qtype[5000][5];
int QidCG[5000],QidnuCG[5000];
float Qx[5][5000];
int atom_number;
int condition;
/******************************************************************/
FILE *op;
char Oatom[10000],Otype_A[10000][5],Otypen_A[10000][5],Ochain[10000];
int Oid[10000],Oidnu[10000];
float Ox[10000],Oy[10000],Oz[10000],Omark1,Omark2;
int N_S;
int Npdb,Nii;
char infileN[1000][20],temp[4],fileN[500][4];
long double RMSD[20];
/*******************************************************************/
int main(int argc, char *argv[])
{
    void Input(void),optimize(),reconstruction();
    int readN(char file_name[1000][20]),readpdb();
    int i;
    Input();
    inpdb=fopen(argv[1],"r+");
    outpdb=fopen("AA_Result.pdb","w+");
           N=readpdb();
           fclose(inpdb);
           if(QtypeACG[1][0]!='P')
           {
                 condition=1;
                 for(i=1;i<=N;i++)
                 {
                   
                   strcpy(atomCG[i+1],QatomCG[i]);
                   idCG[i+1]=QidCG[i];
                   strcpy(typeACG[i+1],QtypeACG[i]);
                   strcpy(type[i+1],Qtype[i]);
                   strcpy(chainCG[i+1],QchainCG[i]);
                   idnuCG[i+1]=QidnuCG[i];
                   x[1][i+1]=Qx[1][i];
                   x[2][i+1]=Qx[2][i];
                   x[3][i+1]=Qx[3][i];
                 }
              strcpy(atomCG[1],QatomCG[1]);
              idCG[1]=QidCG[1];
              strcpy(typeACG[1],"P");
              strcpy(type[1],Qtype[1]);
              strcpy(chainCG[1],QchainCG[1]);
              idnuCG[1]=QidnuCG[1];
              x[1][1]=Qx[1][1]+2.00;
              x[2][1]=Qx[2][1]+2.00;
              x[3][1]=Qx[3][1]+2.00;

              strcpy(atomCG[N+1],QatomCG[N]);
              idCG[N+1]=QidCG[N];
              strcpy(typeACG[N+1],"P");
              strcpy(type[N+1],Qtype[N]);
              strcpy(chainCG[N+1],QchainCG[N]);
              idnuCG[N+1]=QidnuCG[N];
              x[1][N+2]=Qx[1][N]+2.00;
              x[2][N+2]=Qx[2][N]+2.00;
              x[3][N+2]=Qx[3][N]+2.00;
              N=N+2;
    }
    else
    { 
            condition=0;
            for(i=1;i<=N;i++)
            {
                   
                   strcpy(atomCG[i],QatomCG[i]);
                   idCG[i]=QidCG[i];
                   strcpy(typeACG[i],QtypeACG[i]);
                   strcpy(type[i],Qtype[i]);
                   strcpy(chainCG[i],QchainCG[i]);
                   idnuCG[i]=QidnuCG[i];
                   x[1][i]=Qx[1][i];
                   x[2][i]=Qx[2][i];
                   x[3][i]=Qx[3][i];
              }
              strcpy(atomCG[N+1],QatomCG[N]);
              idCG[N+1]=QidCG[N];
              strcpy(typeACG[N+1],"P");
              strcpy(type[N+1],Qtype[N]);
              strcpy(chainCG[N+1],QchainCG[N]);
              idnuCG[N+1]=QidnuCG[N];
              x[1][N+1]=Qx[1][N]+2.00;
              x[2][N+1]=Qx[2][N]+2.00;
              x[3][N+1]=Qx[3][N]+2.00;
              N=N+1;
              
   }


         reconstruction();
         optimize(); 
         fclose(outpdb);   


    return 0;
}


void reconstruction()
{


    void Assemble();
    atom_number=1;
   
    Assemble();
    

}
void Input(void)
{
    int i,ii;
     char filename[40];
     for(ii=1;ii<=nm_frag;ii++)
     {
                sprintf(filename,"fragment/A/fragA%d.pdb",ii); fragA[ii]=fopen(filename,"r+");
                sprintf(filename,"fragment/G/fragG%d.pdb",ii); fragG[ii]=fopen(filename,"r+");
                sprintf(filename,"fragment/C/fragC%d.pdb",ii); fragC[ii]=fopen(filename,"r+");
                sprintf(filename,"fragment/U/fragU%d.pdb",ii); fragU[ii]=fopen(filename,"r+");

        i = 0;
    while(!feof(fragA[ii]))
    {
        i++;
        fscanf(fragA[ii],"%s %d %s %s %s %d %f %f %f %s %s %s\n",&atom[ii][i],&id[ii],type_A[ii][i],typen_A[ii][i],&chain[ii],&idnu[ii],&x_A[ii][1][i],&x_A[ii][2][i],&x_A[ii][3][i],&mark1,&mark2,&mark3);
    }
    NA[ii]=i;
  
    i = 0;
    while(!feof(fragG[ii]))
    {
        i++;
        fscanf(fragG[ii],"%s %d %s %s %s %d %f %f %f %s %s %s\n",&atom[ii][i],&id[ii],type_G[ii][i],typen_G[ii][i],&chain[ii],&idnu[ii],&x_G[ii][1][i],&x_G[ii][2][i],&x_G[ii][3][i],&mark1,&mark2,&mark3); 
    }
    NG[ii]=i;
    i = 0;
    while(!feof(fragC[ii]))
    {
         i++;
         fscanf(fragC[ii],"%s %d %s %s %s %d %f %f %f %s %s %s\n",&atom[ii][i],&id[ii],type_C[ii][i],typen_C[ii][i],&chain[ii],&idnu[ii],&x_C[ii][1][i],&x_C[ii][2][i],&x_C[ii][3][i],&mark1,&mark2,&mark3);
    }
    NC[ii]=i;
    i = 0;
    while(!feof(fragU[ii]))
    {
         i++;
         fscanf(fragU[ii],"%s %d %s %s %s %d %f %f %f %s %s %s\n",&atom[ii][i],&id[ii],type_U[ii][i],typen_U[ii][i],&chain[ii],&idnu[ii],&x_U[ii][1][i],&x_U[ii][2][i],&x_U[ii][3][i],&mark1,&mark2,&mark3);
    }
    NU[ii]=i;          
   fclose(fragA[ii]);
   fclose(fragG[ii]);
   fclose(fragC[ii]);
   fclose(fragU[ii]);           
     }   
    
    
     
   
}
void Assemble()
{
  int i,j,k,kk,ii;
  void Rotate();
  void Replace(int kk);
  long double min;
  for(i=1;i<=N;i++)
  {
      if(fmod(i,3)==0)
      {
          for(j=1;j<=3;j++)
          {    
               
                     y_CG[j][1]=x[j][i-2]; y_CG[j][2]=x[j][i-1]; y_CG[j][3]=x[j][i]; y_CG[j][4]=x[j][i+1];     //粗粒化单个核苷酸片段的坐标y_CG；
                
          }
//////////////G////////////
        for(ii=1;ii<=nm_frag;ii++)
        {
          if(strcmp(type[i],"G")==0) 
          {
                 N_AA[ii]=NG[ii];
                 for(j=1; j<=3; j++)
                 {
                    
                      x_CG[ii][j][1]=x_G[ii][j][1]; 
                      x_CG[ii][j][2]=x_G[ii][j][6]; 
                      x_CG[ii][j][3]=x_G[ii][j][13];  
                      x_CG[ii][j][4]=x_G[ii][j][24];                 
 
                  }
                  for(k=1;k<=N_AA[ii];k++)
                  {
                        atom_AA[ii][k]=i/3+k-1; strcpy(type_AA[ii][k],type_G[ii][k]); strcpy(typen_AA[ii][k],typen_G[ii][k]); nucl_AA=i/3;
                        for(j=1;j<=3;j++)  
                        {
                                x_AA[ii][j][k]=x_G[ii][j][k];
                        }
                  }
           }
//////////////A////////////
           else if(strcmp(type[i],"A")==0) 
           { 
                  N_AA[ii]=NA[ii];
                  for(j=1; j<=3; j++)
                  { 
                             x_CG[ii][j][1]=x_A[ii][j][1]; 
                             x_CG[ii][j][2]=x_A[ii][j][6]; 
                             x_CG[ii][j][3]=x_A[ii][j][13];  
                             x_CG[ii][j][4]=x_A[ii][j][23];                       
                  }
                  for(k=1;k<=N_AA[ii];k++)
                  {
                           atom_AA[ii][k]=i/3+k-1; strcpy(type_AA[ii][k],type_A[ii][k]); strcpy(typen_AA[ii][k],typen_A[ii][k]); nucl_AA=i/3;
                           for(j=1;j<=3;j++)  
                           {
                                  x_AA[ii][j][k]=x_A[ii][j][k];
                           }
                   }
            }
//////////////C////////////
            else if(strcmp(type[i],"C")==0) 
            {
                     N_AA[ii]=NC[ii];
                     for(j=1; j<=3; j++)
                     {

                     
                           x_CG[ii][j][1]=x_C[ii][j][1]; 
                           x_CG[ii][j][2]=x_C[ii][j][6]; 
                           x_CG[ii][j][3]=x_C[ii][j][13];  
                           x_CG[ii][j][4]=x_C[ii][j][21]; 
                            
                     }
                     for(k=1;k<=N_AA[ii];k++)
                     {
                            atom_AA[ii][k]=i/3+k-1; strcpy(type_AA[ii][k],type_C[ii][k]); strcpy(typen_AA[ii][k],typen_C[ii][k]); nucl_AA=i/3;
                            for(j=1;j<=3;j++)  
                            {
                                   x_AA[ii][j][k]=x_C[ii][j][k];
                             }
                      }
             }
//////////////U////////////
             else 
             {
                      N_AA[ii]=NU[ii];
                      for(j=1; j<=3; j++)
                      {
        
                              x_CG[ii][j][1]=x_U[ii][j][1]; 
                              x_CG[ii][j][2]=x_U[ii][j][6]; 
                              x_CG[ii][j][3]=x_U[ii][j][13]; 
                              x_CG[ii][j][4]=x_U[ii][j][21]; 
                            
                      }
                      for(k=1;k<=N_AA[ii];k++)
                      {
                             atom_AA[ii][k]=i/3+k-1; strcpy(type_AA[ii][k],type_U[ii][k]); strcpy(typen_AA[ii][k],typen_U[ii][k]); nucl_AA=i/3;
                             for(j=1;j<=3;j++)  
                             {
                                         x_AA[ii][j][k]=x_U[ii][j][k];
                             }
                       }
               }
                Rotate(x_CG,y_CG,ii);    //用已有全原子片段重合替换粗粒化核苷酸；
    }
       min=RMSD[1];
       for(ii=1;ii<=nm_frag;ii++)
       {
             if(RMSD[ii]<=min)
             {
                    min=RMSD[ii];
                    kk=ii;
             }
       }
       Replace(kk);
       }
    } 
}

void Rotate(float xx_CG[10][5][5],float yy_CG[5][5],int ii)
{
  int         i,j,k,n;
  float       max, min, unit, xnew_CG[5][5];
  double      sigma, sigma0,xnew_CG_i;
 
//////////////////初始化////////////
   for(i=0;i<=4;i++)       //ininalization of matrix;
   {
          xmiddle[ii][i]=0.0; ymiddle[i]=0.0;
          for(j=0;j<=4;j++)
          {
                  R[i][j]=0.0; R_T[i][j]=0.0; Tao[i][j]=0.0; //U[i][j]=0.0; B[i][j]=0.0;
          }
    }

         RMSD[ii]=0.0;
    
/////////////////////中心化///////////////
   for(i=1;i<=4;i++)
   {
         xmiddle[ii][1] += xx_CG[ii][1][i]; xmiddle[ii][2] += xx_CG[ii][2][i]; xmiddle[ii][3] += xx_CG[ii][3][i];    
         ymiddle[1] += yy_CG[1][i]; ymiddle[2] += yy_CG[2][i]; ymiddle[3] += yy_CG[3][i];    
   } 
   xmiddle[ii][1] /= 4.0; xmiddle[ii][2] /= 4.0; xmiddle[ii][3] /= 4.0; 
   ymiddle[1] /= 4.0; ymiddle[2] /= 4.0; ymiddle[3] /= 4.0; //几何中心
   for(i=1; i<=4; i++)
   {   
        for(j=1; j<=3; j++)
        {        
            xx_CG[ii][j][i] -= xmiddle[ii][j];    //各自的几何中心移动到0点
            yy_CG[j][i] -= ymiddle[j];    
         } 

    }  
/////////////计算旋转矩阵//////////////
    for(i=1; i<=3; i++)
    {
        for(j=1; j<=3; j++)
        {            
            for(k=1; k<=4; k++)
            {
                R[i][j] += yy_CG[i][k]*xx_CG[ii][j][k]*w;  //w取值如何定？
            }       
         }   
     }
     for(i=1; i<=3; i++)
     {
        for(j=1; j<=3; j++)
        {
            
            R_T[i][j] = R[j][i];
         }
     }    
     for(i=1; i<=3; i++)
     {
        for(j=1; j<=3; j++)
        {
            
            for(k=1; k<=3; k++)
            {
                Tao[i][j] += R_T[i][k]*R[k][j];
            }            
         }
      }
/////////////////////////本征值求解////////////////////////////
      min = -100.; max = 10000.; unit = 0.0001; sigma0 = 0; n = 0;   dis=0.0; 
      lambda = min; 
      do
      {
        //解特征值，这样看可能比较难理解。其实这里就是求特征值中的求行列式
        sigma = (Tao[1][1]-lambda)*(Tao[2][2]-lambda)*(Tao[3][3]-lambda) + Tao[1][2]*Tao[2][3]*Tao[3][1] + Tao[1][3]*Tao[2][1]*Tao[3][2] - Tao[1][3]*Tao[3][1]*(Tao[2][2]-lambda) - Tao[1][2]*Tao[2][1]*(Tao[3][3]-lambda) - Tao[2][3]*Tao[3][2]*(Tao[1][1]-lambda);              
        
        if(sigma * sigma0 < 0)      //前后两次计算的sigma相乘为0意味着两个sigma负号不同，所以解（过0点）一定在两个sigma之间
        {
            n++;
            eigenvalue[n] = lambda - unit/2.;       //求得特征值lambda后，记录下这个特征值eigenvalue[]            
        }
        sigma0 = sigma;
        lambda += unit;
        
       }
       while( !(n==3 || lambda > max) );       //求完三个特征值就跳出，后面那个跳出条件我忘了是啥意思了。。
      for(i=0; i<=4; i++)
      {
           for(j=0; j<=4; j++)
           {
                A[i][j] = 0.;  B[i][j]=0.;U[ii][i][j]=0.; xnew_CG[i][j]=0.; //xnew[i][k]=0.; //初始化
           }
       }
       for(i=1; i<=3; i++)	  //计算旋转矩阵，就是把三个本征矢量塞进一个3×3矩阵里面。注意，这里三个本征矢量的顺序将决定后面把哪一根轴转成x，哪一根转成z
       {
          A[1][i] = 1.;      //解本征矢本征不需要三个变量，因此将第一个值定为1,其实定为其他也可以，噢，不能为0
          A[3][i] = ( Tao[2][1] + (Tao[2][2] - eigenvalue[i])*(eigenvalue[i]-Tao[1][1])/Tao[1][2] ) / ( Tao[1][3]*(Tao[2][2]-eigenvalue[i])/Tao[1][2] - Tao[2][3]  );        //看着很复杂，找张纸推导一下就可以了
          A[2][i] = ( eigenvalue[i]-Tao[1][1]-Tao[1][3] * A[3][i] ) / Tao[1][2];            
       }
       for(i=1; i<=3; i++)
       {
        
           dis = sqrt( A[1][i]*A[1][i] + A[2][i]*A[2][i] + A[3][i]*A[3][i]  ); 
           A[1][i] /= dis;        //注意，这个矩阵是由本征矢合并成的本征矩阵
           A[2][i] /= dis;
           A[3][i] /= dis;       
        //   test = Tao[3][1] * A[1][i] + Tao[3][2] * A[2][i] + (Tao[3][3] - eigenvalue[i]) * A[3][i]; //解方程用前两条，检验用第三条，会有误差，主要来源于数值解法的本征矢        
//       printf("test if = 0    test = %f\n", test);         //越接近0,误差越小     
        }
    
        for(i=1; i<=3; i++)
        {
             for(j=1; j<=3; j++)
             {
                 for(k=1; k<=3; k++)
                 {
                        B[j][i] += R[j][k]*A[k][i]/ sqrt(eigenvalue[i]);      //求B矩阵
                 }               
             }
         }
    
//    printf("\nthe U matrix\n");
         for(i=1; i<=3; i++)
         {
               for(j=1; j<=3; j++)
               {
                     for(k=1; k<=3; k++)
                     {          
                         U[ii][i][j] += B[i][k]*A[j][k];           //求旋转矩阵U    
                     }
               }
          }
///////////////////旋转整个片段，以尽可能重合/////////
          for(k=1; k<=4; k++)
          {
                dis_r = 0.;
                for(i=1; i<=3; i++)
                {
                      xnew_CG_i=0.; 
                      for(j=1; j<=3; j++)
                      {
                             xnew_CG_i += U[ii][i][j]*xx_CG[ii][j][k];  
                      }  
                      xnew_CG[i][k]=xnew_CG_i;
                      dis_r += (xnew_CG[i][k]-yy_CG[i][k])*(xnew_CG[i][k]-yy_CG[i][k]);      
                }
                RMSD[ii] += dis_r;    
           }    
           RMSD[ii] = sqrt(RMSD[ii]/4.0);    
  
           for(k=1;k<=4; k++)
           {
               for(j=1; j<=3; j++)
               {
                    xnew_CG[j][k] += ymiddle[j];      //各自的几何中心移动到0点
                    yy_CG[j][k] += ymiddle[j];        
                }   
            }
}

void Replace(int ii)
{
  int     i,j,k; 
  float   xnew[5][50];

      for(k=1;k<=N_AA[ii];k++)
      {
           for(i=1;i<=3;i++)
           {
                x_AA[ii][i][k] -= xmiddle[ii][i];   xnew[i][k]=0.;
           }  
      }

     for(k=1;k<=N_AA[ii];k++)
     {     
           for(i=1;i<=3;i++)
           {
    
                for(j=1;j<=3;j++)
                {
                     xnew[i][k] += U[ii][i][j]*x_AA[ii][j][k]; 
                }   
                xnew[i][k]=xnew[i][k]+ymiddle[i];     
            }   
     }  
     for(k=1;k<=N_AA[ii]-3;k++) 
     {
               
              
               Oid[atom_number]=atom_number;
               strcpy(Otype_A[atom_number],type_AA[ii][k]);
               strcpy(Otypen_A[atom_number],typen_AA[ii][k]);
               Oidnu[atom_number]=nucl_AA;
               Ox[atom_number]=xnew[1][k];
               Oy[atom_number]=xnew[2][k];
               Oz[atom_number]=xnew[3][k];
               atom_number++;
     
               
     }
     
}



void optimize()
{
     int i=1,number;
     float centerx,centery,centerz;
     float allx=0.0,ally=0.0,allz=0.0;

     number=atom_number-1;
   //  printf("%d\n",number);
     for(i=1;i<=number;i++)
     {
            allx=allx+Ox[i];
            ally=ally+Oy[i];
            allz=allz+Oz[i];
    }
    centerx=allx/number;
    centery=ally/number;
    centerz=allz/number;
    for(i=1;i<=number;i++)
    {
      Ox[i]=Ox[i]-centerx;
      Oy[i]=Oy[i]-centery;
      Oz[i]=Oz[i]-centerz;
   }
 
   if(condition==1)
   {       
     for(i=4;i<=number;i++)
     {
         
         fprintf(outpdb,"%-6s%5d  %-4s %2s %s%4d %11.3f%8.3f%8.3f\n","ATOM",Oid[i],Otype_A[i],Otypen_A[i],"A",Oidnu[i],Ox[i],Oy[i],Oz[i]); 
     }
   }
   else
   {       
     for(i=1;i<=number;i++)
     {
         
         fprintf(outpdb,"%-6s%5d  %-4s %2s %s%4d %11.3f%8.3f%8.3f\n","ATOM",Oid[i],Otype_A[i],Otypen_A[i],"A",Oidnu[i],Ox[i],Oy[i],Oz[i]); 
     }
   } 

}

int readpdb()
{

    char  numl1[10000][10],numl2[10000][10];
    char x1[10000][10], y1[10000][10], z1[10000][10];
    char a[500];
    int i,j;
    i=1;
    memset(x1, 0, sizeof(x1));
    memset(y1, 0, sizeof(y1));
    memset(z1, 0, sizeof(z1));
    while(fgets(a,500,inpdb)!=NULL)
    {
        sprintf(QatomCG[i],"%c%c%c%c",a[0],a[1],a[2],a[3]);
        sprintf(numl1[i],"%c%c%c%c",a[8],a[9],a[10],a[11]);
        QidCG[i]=atof(numl1[i]);
        sprintf(QtypeACG[i],"%c%c%c",a[13],a[14],a[15]);
        sprintf(Qtype[i],"%c",a[19]);//residue_type
        sprintf(QchainCG[i],"%c",a[21]);//chain_type
        sprintf(numl2[i],"%c%c%c%c",a[22],a[23],a[24],a[25]);//residue_number
        QidnuCG[i]=atof(numl2[i]);
        sprintf(x1[i],"%c%c%c%c%c%c%c%c",a[30],a[31],a[32],a[33],a[34],a[35],a[36],a[37]);//x_coordinate
        Qx[1][i]=atof(x1[i]);
        sprintf(y1[i],"%c%c%c%c%c%c%c%c",a[38],a[39],a[40],a[41],a[42],a[43],a[44],a[45]);//y_coordinate
        Qx[2][i]=atof(y1[i]);
        sprintf(z1[i],"%c%c%c%c%c%c%c%c",a[46],a[47],a[48],a[49],a[50],a[51],a[52],a[53]);//z_coordinate
        Qx[3][i]=atof(z1[i]);
        i++;
     }
     memset(a,0,sizeof(a));
     j=i-1;
     return j;
}


