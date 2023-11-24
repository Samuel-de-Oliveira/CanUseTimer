/*  ** Windows runner for CanUseTimer **
 *
 * This program basically open the Main.py
 * files on Windows, using a portable Python
 * version.
 * 
 * * Created by: Samuel de  Oliveira (Github: Samuel-de-Oliveira)
 * 
 */

#include <stdio.h>

int main() {
    int exit = system(".\\Python\\python.exe Main.py");
    if (exit) {
        printf("Woops... something gone wrong!\nPlease show this error to the developer.\n");
        system("pause");
    }
    return 0;
}
