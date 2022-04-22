#include<stdio.h>
#include<math.h>
#include<dirent.h>
#include<sys/types.h>
#include<sys/stat.h>
#include<time.h>
#include<string.h>
#include<stdlib.h>
#define e 0.26


float kpc=60,lpc=3.92,kcp=33,lcp=3.9,kcN=24.8,lcN=3.346;                                      //Bond
float kpcp=6.3,Apcp=1.82,kcpc=15.3,Acpc=1.8,kpcN=9.75,ApcN=1.64,kNcp=15.23,ANcp=1.66;        //Angle
float kpcpc=0.8,dpcpc=2.56,kcpcp=3.6,dcpcp=-2.94,kcpcN=0.825,dcpcN=-1.164,kNcpc=0.76,dNcpc=0.88; //Dihedral



double ***read_potential(char potential_file[], int intervals)
{
 int i, j;
 double ***p=(double ***)malloc(12*sizeof(double**));

 for(i=0;i<12;i++) 
  p[i]=(double **)malloc(12*sizeof(double*));
 
 for(i=0;i<12;i++)
  for(j=0;j<12;j++)
   p[i][j]=(double *)malloc(intervals*sizeof(double));

 FILE *p_f;
 int n1, n2, n3, nnn;

 p_f=fopen(potential_file,"r+");
 while(!feof(p_f))
 {
  for(n1=0;n1<12;n1++)
   for(n2=0;n2<12;n2++)
    for(n3=0;n3<intervals;n3++)
     fscanf(p_f,"%d %d %d %lf\n",&nnn,&nnn,&nnn,&p[n1][n2][n3]);
 }
 fclose(p_f);

 if(intervals != n3)
 {
  printf("Error---loading_potential---Error!\n");
  exit(-1);          
 }
 return p;
}

int open_dir(char file_name[][300], char file_name1[][300], char route[])
{
  DIR *dir;
  struct dirent *ptr;
  int k=0;
  char *c;

  dir=opendir(route);

  while((ptr=readdir(dir))!=NULL)
  {
    c=ptr->d_name;
    while(*c!='\0')
     c++;

   if(strcmp((c-4),".pdb")==0 && strcmp((c-7),".pdb")!=0)
   {
    sprintf(file_name[k],"%s",ptr->d_name);
    sprintf(file_name1[k],"%s/%s",route,ptr->d_name);
    k++;
   }
  }
   closedir(dir);
   return k;
}

int read_pdb(char pdb_file[300], char type1[][5], char type2[][5], char type[][10], char chain[][5], char num[][10], float x[], float y[], float z[], int L)
{
 FILE *pdb_f;
 char aline[500], x1[L][10], y1[L][10], z1[L][10];
 int i, cc1, cc2, lll;

 pdb_f=fopen(pdb_file,"r+");
 
 i=0;
 memset(x1, 0, sizeof(x1));
 memset(y1, 0, sizeof(y1));
 memset(z1, 0, sizeof(z1));
 while(fgets(aline,500,pdb_f)!=NULL)
 {
  if(aline[0]=='A' && aline[1]=='T' && aline[2]=='O' && aline[3]=='M')
  {
   sprintf(type1[i],"%c%c%c",aline[13],aline[14],aline[15]);//atom_type
   if(type1[i][0]==' ')
    for(cc1=1;cc1<strlen(type1[i]);cc1++)
     if(type1[i][cc1]!=' ')
     {
      for(cc2=cc1;cc2<strlen(type1[i]);cc2++)
       type1[i][cc2-cc1]=type1[i][cc2];
      type1[i][cc2-1]='\0';
      break;
     }
   sprintf(type2[i],"%c",aline[19]);//residue_type
   sprintf(chain[i],"%c",aline[21]);//chain_type

   sprintf(num[i],"%c%c%c%c",aline[22],aline[23],aline[24],aline[25]);//residue_number
   sprintf(x1[i],"%c%c%c%c%c%c%c%c",aline[30],aline[31],aline[32],aline[33],aline[34],aline[35],aline[36],aline[37]);//x_coordinate
   x[i]=atof(x1[i]);
   sprintf(y1[i],"%c%c%c%c%c%c%c%c",aline[38],aline[39],aline[40],aline[41],aline[42],aline[43],aline[44],aline[45]);//y_coordinate
   y[i]=atof(y1[i]);
   sprintf(z1[i],"%c%c%c%c%c%c%c%c",aline[46],aline[47],aline[48],aline[49],aline[50],aline[51],aline[52],aline[53]);//z_coordinate
   z[i]=atof(z1[i]);

   sprintf(type[i],"%s%s",type2[i],type1[i]);
   for(lll=0;lll<strlen(type[i]);lll++)
    if(type[i][lll]==' ')
     type[i][lll]='\0';

   i++;
  }
  memset(aline,0,sizeof(aline));
 }
 fclose(pdb_f);
 return i;
}

double fun(int n)
{
 return -355.0/sqrt(n+16) + 72.0;
}

int main(int argc, char *argv[])
{
 clock_t start,end;
 start=clock();

 float spendtime;

 int k1, k2, k3, k4, intervals1, intervals2, intervals3, intervals4, iii;
 double Rc1, Rc2, Rc3, Rc4;
 k1=0; k2=1; k3=2; k4=4;
 Rc1=5.0; Rc2=9.0; Rc3=13.0; Rc4=24.0;
 intervals1=17; intervals2=30; intervals3=43; intervals4=80;

//atomtype
/////////////////////////////////////////////////////////
 char atomtype[12][6];
 FILE *atom_type;
 iii=0;
 memset(atomtype,0,sizeof(atomtype));
 atom_type=fopen("data/12atom_type.dat","r+");
 while(!feof(atom_type))
 {
  fscanf(atom_type,"%s\n",atomtype[iii]);
  iii++;
 }
 fclose(atom_type);

//restype
 char restype[4][2]={"A", "U", "C", "G"};

 int n33, n44, nums[4], nume[4];
 nums[0]=0; nume[0]=3;
 nums[1]=3; nume[1]=6;
 nums[2]=6; nume[2]=9;
 nums[3]=9; nume[3]=12;

/////////////////////////////////////////////////////////
//potential
/////////////////////////////////////////////////////////
 double ***potential1, ***potential2, ***potential3, ***potential4;
 potential1 = read_potential("data/0-1_short-ranged.potential", intervals1);
 potential2 = read_potential("data/1-2_short-ranged.potential", intervals2);
 potential3 = read_potential("data/2-4_short-ranged.potential", intervals3);
 potential4 = read_potential("data/long-ranged.potential", intervals4);
/////////////////////////////////////////////////////////

//read_pdb
/////////////////////////////////////////////////////////
 FILE *pdb_f, *FP;
 int n1, n2, n3, n4, nnn, NNN, length, Len, number;
 number=atoi(argv[2]);
 char aline[500], file_name[number][300], file_name1[number][300];
 double distance, energy, energy1, energy2, energy3, energy4;

 memset(file_name,0,sizeof(file_name));
 memset(file_name1,0,sizeof(file_name1));
 NNN=open_dir(file_name, file_name1, argv[1]);

 FP = fopen(argv[3],"w+");

 for(nnn=0;nnn<NNN;nnn++)
 {
 pdb_f=fopen(file_name1[nnn],"r+");
 Len=0;
 memset(aline,0,sizeof(aline));
 while(fgets(aline,500,pdb_f)!=NULL)
 {
  Len++;
  memset(aline,0,sizeof(aline));
 }
 fclose(pdb_f);

 int N;
 char type1[Len][5], type2[Len][5], type[Len][10], chain[Len][5], num[Len][10];
 float x[Len], y[Len], z[Len];
 memset(type1,0,sizeof(type1)); memset(type2,0,sizeof(type2)); memset(type,0,sizeof(type));
 memset(chain,0,sizeof(chain));
 memset(num,0,sizeof(num));
 memset(x,0,sizeof(x)); memset(y,0,sizeof(y)); memset(z,0,sizeof(z));

 N=read_pdb(file_name1[nnn], type1, type2, type, chain, num, x, y, z, Len);
/////////////////////////////////////////////////////////
//obtainig_energy
/////////////////////////////////////////////////////////

 energy=0.0; energy1=0.0; energy2=0.0; energy3=0.0; energy4=0.0;
 for(n1=0;n1<N;n1++)
  for(n2=n1+1;n2<N;n2++)
   if(strcmp(num[n1], num[n2])!=0 || strcmp(chain[n1], chain[n2])!=0)
    for(n33=0;n33<4;n33++)
     if(strcmp(type2[n1],restype[n33])==0)
     {
      for(n3=nums[n33];n3<nume[n33];n3++)
       if(strcmp(type[n1],atomtype[n3])==0)
       {
        for(n44=0;n44<4;n44++)
         if(strcmp(type2[n2],restype[n44])==0)
         {
          for(n4=nums[n44];n4<nume[n44];n4++)
           if(strcmp(type[n2],atomtype[n4])==0)
           {
            distance=sqrt((x[n1]-x[n2])*(x[n1]-x[n2])+(y[n1]-y[n2])*(y[n1]-y[n2])+(z[n1]-z[n2])*(z[n1]-z[n2]));
///         
            if(abs(atoi(num[n1])-atoi(num[n2]))>k4 || strcmp(chain[n1], chain[n2])!=0)//long-ranged
            {
             //if(distance>0 && distance<=Rc4)
             if((int)(distance/0.3)<intervals4)
              energy4+=potential4[n3][n4][(int)(distance/0.3)]; 
            }
///
///
             else if(abs(atoi(num[n1])-atoi(num[n2]))>k1 && abs(atoi(num[n1])-atoi(num[n2]))<=k2 && strcmp(chain[n1], chain[n2])==0)//short-ranged
            {
             //if(distance>0 && distance<=Rc1)
            if((int)(distance/0.3)<intervals1)
             energy1+=potential1[n3][n4][(int)(distance/0.3)];
            }
///
///
            else if(abs(atoi(num[n1])-atoi(num[n2]))>k2 && abs(atoi(num[n1])-atoi(num[n2]))<=k3 && strcmp(chain[n1], chain[n2])==0)//short-ranged
           {
            //if(distance>0 && distance<=Rc2)
            if((int)(distance/0.3)<intervals2)
             energy2+=potential2[n3][n4][(int)(distance/0.3)];
           }
///
           else if(abs(atoi(num[n1])-atoi(num[n2]))>k3 && abs(atoi(num[n1])-atoi(num[n2]))<=k4 && strcmp(chain[n1], chain[n2])==0)//short-ranged
           {
            //if(distance>0 && distance<=Rc3)
            if((int)(distance/0.3)<intervals3)
             energy3+=potential3[n3][n4][(int)(distance/0.3)];
           }
///
          break;
         }
        break;
       }
      break;
     }
    break;
   }

 length=1;
 for(n1=0;n1<N-1;n1++)
  if(strcmp(type2[n1],type2[n1+1])!=0 || strcmp(num[n1],num[n1+1])!=0 || strcmp(chain[n1],chain[n1+1])!=0)
   length++; 
  

     float ex[10000], ey[10000], ez[10000],u0,ub=0.0;
     int N0,ei;
     float PC(),CP(),CN(),PCP(),CPC(),PCN(),NCP(),PCPC(),CPCP(),CPCN(),NCPC();
     if(type1[0][0]=='P')
     {
             
           for(n1=0;n1<N-2;n1++)
           {
                    ex[n1+1]=x[n1];ey[n1+1]=y[n1];ez[n1+1]=z[n1];
           }
           N0=N-2;
     }
     if(type1[2][0]=='P')
     {
           for(n1=2;n1<N-2;n1++)
           {
                     ex[n1-1]=x[n1];ey[n1-1]=y[n1];ez[n1-1]=z[n1];
           } 
           N0=N-4;
     }
     for (ei=1;ei<=N0;ei++)  
     {
        u0=0.0;
        if (fmod(ei,3)==0)  
        {
                if (ei==3)   
                {
                    u0=PC(ei,ex,ey,ez)+CP(ei,ex,ey,ez)+CN(ei,ex,ey,ez)+PCP(ei,ex,ey,ez)+CPC(ei,ex,ey,ez)+PCN(ei,ex,ey,ez)+NCP(ei,ex,ey,ez)+PCPC(ei,ex,ey,ez)+CPCP(ei,ex,ey,ez)+NCPC(ei,ex,ey,ez);
                }
                else if (ei==(N0-1))  
                {
                    u0=PC(ei,ex,ey,ez)+CP(ei,ex,ey,ez)+CN(ei,ex,ey,ez)+PCP(ei,ex,ey,ez)+PCN(ei,ex,ey,ez)+NCP(ei,ex,ey,ez)+CPCN(ei,ex,ey,ez);
                } 
                else 
                {
                    u0=PC(ei,ex,ey,ez)+CP(ei,ex,ey,ez)+CN(ei,ex,ey,ez)+PCP(ei,ex,ey,ez)+CPC(ei,ex,ey,ez)+PCN(ei,ex,ey,ez)+NCP(ei,ex,ey,ez)+PCPC(ei,ex,ey,ez)+CPCP(ei,ex,ey,ez)+CPCN(ei,ex,ey,ez)+NCPC(ei,ex,ey,ez);
                }
                ub=ub+u0*0.5963;
          }
      } 

    energy = 1.0*energy1 + 1.0*energy2 + 6.0*energy3 + 8.0*energy4/fun(length)+0.01*ub;
 
 fprintf(FP,"%s,%lf\n", file_name[nnn],energy);
printf("%s\n", file_name[nnn]);
 }
 fclose(FP);
/////////////////////////////////////////////////////////

  int i, j;
  for(i=0;i<12;i++)
   for(j=0;j<12;j++)
    free(potential1[i][j]);
  for(i=0;i<12;i++)
   free(potential1[i]);
  free(potential1);

  for(i=0;i<12;i++)
   for(j=0;j<12;j++)
    free(potential2[i][j]);
  for(i=0;i<12;i++)
   free(potential2[i]);
  free(potential2);

  for(i=0;i<12;i++)
   for(j=0;j<12;j++)
    free(potential3[i][j]);
  for(i=0;i<12;i++)
   free(potential3[i]);
  free(potential3);

  for(i=0;i<12;i++)
   for(j=0;j<12;j++)
    free(potential4[i][j]);
  for(i=0;i<12;i++)
   free(potential4[i]);
  free(potential4);

  end = clock();
  spendtime = (float)(end-start)/(CLOCKS_PER_SEC);
  printf("the spendtime is %f s.\n",spendtime);

  return 6;
}




/****************************************************************************/
float PC(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float d,ul;
 d=sqrt((x1[i1-2]-x1[i1-1])*(x1[i1-2]-x1[i1-1])+(y1[i1-2]-y1[i1-1])*(y1[i1-2]-y1[i1-1])+(z1[i1-2]-z1[i1-1])*(z1[i1-2]-z1[i1-1]));
 ul=kpc*(d-lpc)*(d-lpc);
 return ul;
}
float CP(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float d,ul;
 d=sqrt((x1[i1+1]-x1[i1-1])*(x1[i1+1]-x1[i1-1])+(y1[i1+1]-y1[i1-1])*(y1[i1+1]-y1[i1-1])+(z1[i1+1]-z1[i1-1])*(z1[i1+1]-z1[i1-1]));
 ul=kcp*(d-lcp)*(d-lcp);
 return ul;
}
float CN(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float d,ul;
 d=sqrt((x1[i1]-x1[i1-1])*(x1[i1]-x1[i1-1])+(y1[i1]-y1[i1-1])*(y1[i1]-y1[i1-1])+(z1[i1]-z1[i1-1])*(z1[i1]-z1[i1-1]));
 ul=kcN*(d-lcN)*(d-lcN);
 return ul;
}
float PCP(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float d1,d2,d3,w,a1,ue0;
 d1=sqrt((x1[i1-2]-x1[i1-1])*(x1[i1-2]-x1[i1-1])+(y1[i1-2]-y1[i1-1])*(y1[i1-2]-y1[i1-1])+(z1[i1-2]-z1[i1-1])*(z1[i1-2]-z1[i1-1]));
 d2=sqrt((x1[i1-1]-x1[i1+1])*(x1[i1-1]-x1[i1+1])+(y1[i1-1]-y1[i1+1])*(y1[i1-1]-y1[i1+1])+(z1[i1-1]-z1[i1+1])*(z1[i1-1]-z1[i1+1]));
 d3=sqrt((x1[i1+1]-x1[i1-2])*(x1[i1+1]-x1[i1-2])+(y1[i1+1]-y1[i1-2])*(y1[i1+1]-y1[i1-2])+(z1[i1+1]-z1[i1-2])*(z1[i1+1]-z1[i1-2]));
 w=(d1*d1+d2*d2-d3*d3)/(2.0*d1*d2);
 if (w<=-1.0) {a1=3.14;}
 else if (w>=1.0) {a1=0.;}
 else  {a1=acos(w);}
 ue0=kpcp*(a1-Apcp)*(a1-Apcp);   //由nab产生的标准AformRNA中的峰值为1.63，以下的cpc，pcN,Ncp分别为：1.8，1.63，1.68
 return ue0;
}
float CPC(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float d1,d2,d3,w,a1,ue0;
 d1=sqrt((x1[i1-1]-x1[i1+1])*(x1[i1-1]-x1[i1+1])+(y1[i1-1]-y1[i1+1])*(y1[i1-1]-y1[i1+1])+(z1[i1-1]-z1[i1+1])*(z1[i1-1]-z1[i1+1]));
 d2=sqrt((x1[i1+1]-x1[i1+2])*(x1[i1+1]-x1[i1+2])+(y1[i1+1]-y1[i1+2])*(y1[i1+1]-y1[i1+2])+(z1[i1+1]-z1[i1+2])*(z1[i1+1]-z1[i1+2]));
 d3=sqrt((x1[i1+2]-x1[i1-1])*(x1[i1+2]-x1[i1-1])+(y1[i1+2]-y1[i1-1])*(y1[i1+2]-y1[i1-1])+(z1[i1+2]-z1[i1-1])*(z1[i1+2]-z1[i1-1]));
 w=(d1*d1+d2*d2-d3*d3)/(2.0*d1*d2);
 if (w<=-1.0) {a1=3.14;}
 else if (w>=1.0) {a1=0.;}
 else  {a1=acos(w);}
 ue0=kcpc*(a1-Acpc)*(a1-Acpc);   
 return ue0;
}
float PCN(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float d1,d2,d3,w,a1,ue0;
 d1=sqrt((x1[i1-1]-x1[i1-2])*(x1[i1-1]-x1[i1-2])+(y1[i1-1]-y1[i1-2])*(y1[i1-1]-y1[i1-2])+(z1[i1-1]-z1[i1-2])*(z1[i1-1]-z1[i1-2]));
 d2=sqrt((x1[i1-1]-x1[i1])*(x1[i1-1]-x1[i1])+(y1[i1-1]-y1[i1])*(y1[i1-1]-y1[i1])+(z1[i1-1]-z1[i1])*(z1[i1-1]-z1[i1]));
 d3=sqrt((x1[i1-2]-x1[i1])*(x1[i1-2]-x1[i1])+(y1[i1-2]-y1[i1])*(y1[i1-2]-y1[i1])+(z1[i1-2]-z1[i1])*(z1[i1-2]-z1[i1]));
 w=(d1*d1+d2*d2-d3*d3)/(2.0*d1*d2);
 if (w<=-1.0) {a1=3.14;}
 else if (w>=1.0) {a1=0.;}
 else  {a1=acos(w);}
 ue0=kpcN*(a1-ApcN)*(a1-ApcN);
 return ue0;
}
float NCP(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float d1,d2,d3,w,a1,ue0;
 d1=sqrt((x1[i1-1]-x1[i1])*(x1[i1-1]-x1[i1])+(y1[i1-1]-y1[i1])*(y1[i1-1]-y1[i1])+(z1[i1-1]-z1[i1])*(z1[i1-1]-z1[i1]));
 d2=sqrt((x1[i1-1]-x1[i1+1])*(x1[i1-1]-x1[i1+1])+(y1[i1-1]-y1[i1+1])*(y1[i1-1]-y1[i1+1])+(z1[i1-1]-z1[i1+1])*(z1[i1-1]-z1[i1+1]));
 d3=sqrt((x1[i1+1]-x1[i1])*(x1[i1+1]-x1[i1])+(y1[i1+1]-y1[i1])*(y1[i1+1]-y1[i1])+(z1[i1+1]-z1[i1])*(z1[i1+1]-z1[i1]));
 w=(d1*d1+d2*d2-d3*d3)/(2.0*d1*d2);
 if (w<=-1.0) {a1=3.14;}
 else if (w>=1.0) {a1=0.;}
 else  {a1=acos(w);}
 ue0=kNcp*(a1-ANcp)*(a1-ANcp);
 return ue0;
}
float PCPC(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float c1,c2,c3,p1,p2,p3,e1,f1,pp1,g1,g2,g3,gg1,hh1,di,ud0=0.0;
 c1=((y1[i1-2]-y1[i1-1])*(z1[i1-1]-z1[i1+1])-(z1[i1-2]-z1[i1-1])*(y1[i1-1]-y1[i1+1]));
 c2=((z1[i1-2]-z1[i1-1])*(x1[i1-1]-x1[i1+1])-(x1[i1-2]-x1[i1-1])*(z1[i1-1]-z1[i1+1]));
 c3=((x1[i1-2]-x1[i1-1])*(y1[i1-1]-y1[i1+1])-(y1[i1-2]-y1[i1-1])*(x1[i1-1]-x1[i1+1]));
 p1=((y1[i1-1]-y1[i1+1])*(z1[i1+1]-z1[i1+2])-(z1[i1-1]-z1[i1+1])*(y1[i1+1]-y1[i1+2]));
 p2=((z1[i1-1]-z1[i1+1])*(x1[i1+1]-x1[i1+2])-(x1[i1-1]-x1[i1+1])*(z1[i1+1]-z1[i1+2]));
 p3=((x1[i1-1]-x1[i1+1])*(y1[i1+1]-y1[i1+2])-(y1[i1-1]-y1[i1+1])*(x1[i1+1]-x1[i1+2]));
 e1=sqrt(c1*c1+c2*c2+c3*c3); f1=sqrt(p1*p1+p2*p2+p3*p3);
 pp1=(c1*p1+c2*p2+c3*p3)/(e1*f1);
 g1=(x1[i1-2]-x1[i1+2]); g2=(y1[i1-2]-y1[i1+2]); g3=(z1[i1-2]-z1[i1+2]);
 gg1=sqrt(g1*g1+g2*g2+g3*g3); hh1=(p1*g1+p2*g2+p3*g3)/(f1*gg1);
 if (pp1<=-1.0) {di=-3.14;}
 else if (pp1>=1.0) {di=0.;}
 else if (hh1>=0.) {di=acos(pp1);}
 else {di=-acos(pp1);}
//ud0=1.88*(1-cos(di-2.6))+0.5*1.88*(1-cos(3.*(di-2.6))); //由nab产生的AformRNA中的峰值为2.6，cpcp，cpcN,Ncpc分别为：-2.97，-1.286，0.97
 ud0=kpcpc*((1-cos(di-dpcpc))+0.5*(1-cos(3.*(di-dpcpc))));
 return ud0;
}
float CPCP(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float c1,c2,c3,p1,p2,p3,e1,f1,pp1,g1,g2,g3,gg1,hh1,di,ud0=0.0;
 c1=((y1[i1-1]-y1[i1+1])*(z1[i1+1]-z1[i1+2])-(z1[i1-1]-z1[i1+1])*(y1[i1+1]-y1[i1+2]));
 c2=((z1[i1-1]-z1[i1+1])*(x1[i1+1]-x1[i1+2])-(x1[i1-1]-x1[i1+1])*(z1[i1+1]-z1[i1+2]));
 c3=((x1[i1-1]-x1[i1+1])*(y1[i1+1]-y1[i1+2])-(y1[i1-1]-y1[i1+1])*(x1[i1+1]-x1[i1+2]));
 p1=((y1[i1+1]-y1[i1+2])*(z1[i1+2]-z1[i1+4])-(z1[i1+1]-z1[i1+2])*(y1[i1+2]-y1[i1+4]));
 p2=((z1[i1+1]-z1[i1+2])*(x1[i1+2]-x1[i1+4])-(x1[i1+1]-x1[i1+2])*(z1[i1+2]-z1[i1+4]));
 p3=((x1[i1+1]-x1[i1+2])*(y1[i1+2]-y1[i1+4])-(y1[i1+1]-y1[i1+2])*(x1[i1+2]-x1[i1+4]));
 e1=sqrt(c1*c1+c2*c2+c3*c3); f1=sqrt(p1*p1+p2*p2+p3*p3);
 pp1=(c1*p1+c2*p2+c3*p3)/(e1*f1);
 g1=(x1[i1-1]-x1[i1+4]); g2=(y1[i1-1]-y1[i1+4]); g3=(z1[i1-1]-z1[i1+4]);
 gg1=sqrt(g1*g1+g2*g2+g3*g3); hh1=(p1*g1+p2*g2+p3*g3)/(f1*gg1);
 if (pp1<=-1.0) {di=-3.14;}
 else if (pp1>=1.0) {di=0.;}
 else if (hh1>=0.) {di=acos(pp1);}
 else {di=-acos(pp1);}
 ud0=kcpcp*((1-cos(di-dcpcp))+0.5*(1-cos(3.*(di-dcpcp))));
 return ud0;
}
float CPCN(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float c1,c2,c3,p1,p2,p3,e1,f1,pp1,g1,g2,g3,gg1,hh1,di,ud0=0.0;
 c1=((y1[i1-4]-y1[i1-2])*(z1[i1-2]-z1[i1-1])-(z1[i1-4]-z1[i1-2])*(y1[i1-2]-y1[i1-1]));
 c2=((z1[i1-4]-z1[i1-2])*(x1[i1-2]-x1[i1-1])-(x1[i1-4]-x1[i1-2])*(z1[i1-2]-z1[i1-1]));
 c3=((x1[i1-4]-x1[i1-2])*(y1[i1-2]-y1[i1-1])-(y1[i1-4]-y1[i1-2])*(x1[i1-2]-x1[i1-1]));
 p1=((y1[i1-2]-y1[i1-1])*(z1[i1-1]-z1[i1])-(z1[i1-2]-z1[i1-1])*(y1[i1-1]-y1[i1]));
 p2=((z1[i1-2]-z1[i1-1])*(x1[i1-1]-x1[i1])-(x1[i1-2]-x1[i1-1])*(z1[i1-1]-z1[i1]));
 p3=((x1[i1-2]-x1[i1-1])*(y1[i1-1]-y1[i1])-(y1[i1-2]-y1[i1-1])*(x1[i1-1]-x1[i1]));
 e1=sqrt(c1*c1+c2*c2+c3*c3); f1=sqrt(p1*p1+p2*p2+p3*p3);
 pp1=(c1*p1+c2*p2+c3*p3)/(e1*f1);
 g1=(x1[i1-4]-x1[i1]); g2=(y1[i1-4]-y1[i1]); g3=(z1[i1-4]-z1[i1]);
 gg1=sqrt(g1*g1+g2*g2+g3*g3); hh1=(p1*g1+p2*g2+p3*g3)/(f1*gg1);
 if (pp1<=-1.0) {di=-3.14;}
 else if (pp1>=1.0) {di=0.;}
 else if (hh1>=0.) {di=acos(pp1);}
 else {di=-acos(pp1);}
 ud0=kcpcN*((1-cos(di-dcpcN))+0.5*(1-cos(3.*(di-dcpcN))));
 return ud0;
}
float NCPC(int i1,float x1[1000],float y1[1000],float z1[1000])
{
 float c1,c2,c3,p1,p2,p3,e1,f1,pp1,g1,g2,g3,gg1,hh1,di,ud0=0.0;
 c1=((y1[i1]-y1[i1-1])*(z1[i1-1]-z1[i1+1])-(z1[i1]-z1[i1-1])*(y1[i1-1]-y1[i1+1]));
 c2=((z1[i1]-z1[i1-1])*(x1[i1-1]-x1[i1+1])-(x1[i1]-x1[i1-1])*(z1[i1-1]-z1[i1+1]));
 c3=((x1[i1]-x1[i1-1])*(y1[i1-1]-y1[i1+1])-(y1[i1]-y1[i1-1])*(x1[i1-1]-x1[i1+1]));
 p1=((y1[i1-1]-y1[i1+1])*(z1[i1+1]-z1[i1+2])-(z1[i1-1]-z1[i1+1])*(y1[i1+1]-y1[i1+2]));
 p2=((z1[i1-1]-z1[i1+1])*(x1[i1+1]-x1[i1+2])-(x1[i1-1]-x1[i1+1])*(z1[i1+1]-z1[i1+2]));
 p3=((x1[i1-1]-x1[i1+1])*(y1[i1+1]-y1[i1+2])-(y1[i1-1]-y1[i1+1])*(x1[i1+1]-x1[i1+2]));
 e1=sqrt(c1*c1+c2*c2+c3*c3);
 f1=sqrt(p1*p1+p2*p2+p3*p3);
 pp1=(c1*p1+c2*p2+c3*p3)/(e1*f1);
 g1=(x1[i1]-x1[i1+2]); g2=(y1[i1]-y1[i1+2]); g3=(z1[i1]-z1[i1+2]);
 gg1=sqrt(g1*g1+g2*g2+g3*g3); hh1=(p1*g1+p2*g2+p3*g3)/(f1*gg1);
 if (pp1<=-1.0) {di=-3.14;}
 else if (pp1>=1.0) {di=0.;}
 else if (hh1>=0.) {di=acos(pp1);}
 ud0=kNcpc*((1-cos(di-dNcpc))+0.5*(1-cos(3.*(di-dNcpc))));
 return ud0;
}


