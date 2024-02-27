#include <stdio.h>
#include <stdlib.h>
void getAverage(int pixelArray[], int size);
void getLarge(int pixelArray[], int size);

/*Function finds and displays header values, pixel values as well as file size and maximum greyscale value then prints to file and command prompt*/
int main()
{
    /*arrays*/
    char headerArray[3]={0};                    /*headerArray with 3 memory slots all cleared to 0*/
    int pixelArray[80000]={0};                  /*pixelArray with 80,000 memory slots all cleared to 0*/
    /*variables*/
    int size=80000;
    int i=0,column=0,row=0,pixColumn=0,pixRow=0;
    /*file pointers and file input and output */
    FILE * pixIn_fptr;
    FILE * pixOut_fptr;
    pixIn_fptr = fopen("image1.pgm","r");
    pixOut_fptr = fopen("output_image.pgm","w");

    /*Scans file 3 times and assigns values to headerArray then prints headerArray[0] and headerArray[1] to file*/
    for(i=0; i<2; i++)
    {
        fscanf(pixIn_fptr, " %c", & headerArray[i]);
    }
    fprintf(pixOut_fptr,"%c%c\n",headerArray[0], headerArray[1]);

    /*P2 File Header Error Checking*/
    if(headerArray[0]!='P'||headerArray[1]!='2')
    {
        printf("ERROR INVALID FILE - This program only reads 'P2' .pgm format images.\n" );
    }

    /*Goes through file by looping 80,000 times advancing bit by bit and assigning to "pixelArray[]"*/
    for(i=0;i<80000;i++)
    {
        fscanf(pixIn_fptr,"%d",&pixelArray[i]);
    }

    /*assigns array memory values to variables*/
    column=pixelArray[0];
    row=pixelArray[1];
    size=row*column;         /*multiples variables to add new value to size varivable*/
    /*Print to command prompt screen*/
    printf("Size of the picture = %d\n",size);
    printf("Maximum Greyscale value = %d\n",pixelArray[2]);

    /*function calls*/
    getAverage(pixelArray,size);
    getLarge(pixelArray,size);

    /*Changes values that are less than 150 to 255 and greater than 150 to 0*/
    for(i=0;i<size;i++)
    {
        fscanf(pixIn_fptr,"%d", &pixelArray[i]);
        if (pixelArray[i]<=150)
        {
            pixelArray[i]=255;
        }
        else
        {
            pixelArray[i]=0;
        }
    }
    fprintf(pixOut_fptr,"%d %d\n%d\n",column,row,pixelArray[3]); /*Displays row, column and max grey value to file*/

    i=0; /*resets i*/
    /*Prints values to file using rows and columns*/
    for(pixColumn=0;pixColumn<row;pixColumn++)
    {
        for(pixRow=0;pixRow<column;pixRow++)
        {
            fprintf(pixOut_fptr,"%3d ",pixelArray[i]);
            i++;
        }
        fprintf(pixOut_fptr,"\n");
    }
    fclose(pixIn_fptr); /*Closes file pointer*/
    return 0;
}

/*Displays average number in file by adding "pixelArray[]"value to sum over and over then dividing by an incrememting "counter" variable*/
void getAverage(int pixelArray[], int size)
{
    int i=0, sum=0, counter=0,average=0;
    i=0;
    for( i=0;i<size;i++)
    {
        sum=sum+pixelArray[i];
        counter++;
    }
    average=sum/counter;
    printf("Average of numbers in file = %d\n",average);
}

/*Display the largest number in file by replacing "large" variable when its smaller than value in "pixelArray[]"*/
void getLarge(int pixelArray[], int size)
{
    int i=0, large=0;
    i=3;
    for( i=3; i < size; i++)
    {
        if(large<pixelArray[i])
        {
            large=pixelArray[i];
        }
    }
    printf("Biggest number in the file = %d",large);
}

