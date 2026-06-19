#include <stdio.h>
#include <string.h>

void copy_input(char *input)
{
    char buffer[10];
    strcpy(buffer, input);
}

int main()
{
    char user_input[100];
    scanf("%s", user_input);

    copy_input(user_input);

    return 0;
}
