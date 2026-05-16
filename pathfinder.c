#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>  
#include <windows.h> 

#define WIDTH 10
#define HEIGHT 10

// The Maps
char realMap[HEIGHT][WIDTH];  
char robotMap[HEIGHT][WIDTH]; 


int visited[HEIGHT][WIDTH];
int parentX[HEIGHT][WIDTH];
int parentY[HEIGHT][WIDTH];


int dx[] = {-1, 1, 0, 0};
int dy[] = {0, 0, -1, 1};

void initMaps() {
    // Fill the world with Fog of War
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            realMap[i][j] = '0';
            robotMap[i][j] = '?'; 
        }
    }

    // Build the actual walls in the real room
    realMap[3][3] = '1'; realMap[3][4] = '1'; realMap[3][5] = '1';
    realMap[4][5] = '1'; realMap[5][5] = '1';
}

void fireToFSensor(int rx, int ry, int dirX, int dirY) {
    int lx = rx + dirX;
    int ly = ry + dirY;
    
    while (lx >= 0 && lx < HEIGHT && ly >= 0 && ly < WIDTH) {
        if (realMap[lx][ly] == '1') {
            robotMap[lx][ly] = '1'; // Hit a wall, update memory
            break; 
        } else {
            if (robotMap[lx][ly] == '?') {
                robotMap[lx][ly] = '0'; // Discovered empty space
            }
        }
        lx += dirX;
        ly += dirY;
    }
}

void scanEnvironment(int rx, int ry) {
    for(int i = 0; i < 4; i++) {
        fireToFSensor(rx, ry, dx[i], dy[i]);
    }
}

void printMap(int rx, int ry, int goalX, int goalY) {
    system("cls"); 
    
    printf("\n=== Live SLAM Navigation Map ===\n");
    printf(">> TARGET: X:%d, Y:%d\n", goalX, goalY);
    for (int i = 0; i < HEIGHT; i++) {
        for (int j = 0; j < WIDTH; j++) {
            if (i == rx && j == ry) printf("R "); 
            else if (i == goalX && j == goalY) printf("E "); // Draw End Goal dynamically
            else if (robotMap[i][j] == '?') printf("? "); 
            else if (robotMap[i][j] == '0') printf(". "); 
            else if (robotMap[i][j] == '1') printf("# "); 
            else printf("%c ", robotMap[i][j]);
        }
        printf("\n");
    }
    printf("================================\n");
}

bool calculateNextStep(int startX, int startY, int endX, int endY, int *nextX, int *nextY) {
    int queueX[WIDTH * HEIGHT], queueY[WIDTH * HEIGHT];
    int head = 0, tail = 0;

    for (int i = 0; i < HEIGHT; i++) 
        for (int j = 0; j < WIDTH; j++) 
            visited[i][j] = 0;

    queueX[tail] = startX; queueY[tail] = startY; tail++;
    visited[startX][startY] = 1;
    bool reachedEnd = false;

    while (head < tail) {
        int cx = queueX[head], cy = queueY[head]; head++;
        if (cx == endX && cy == endY) { reachedEnd = true; break; }

        for (int i = 0; i < 4; i++) {
            int nx = cx + dx[i], ny = cy + dy[i];
            
            if (nx >= 0 && nx < HEIGHT && ny >= 0 && ny < WIDTH) {
                if (visited[nx][ny] == 0 && robotMap[nx][ny] != '1') {
                    visited[nx][ny] = 1;
                    parentX[nx][ny] = cx; parentY[nx][ny] = cy;
                    queueX[tail] = nx; queueY[tail] = ny; tail++;
                }
            }
        }
    }

    if (!reachedEnd) return false;

    int cx = endX, cy = endY;
    while (!(parentX[cx][cy] == startX && parentY[cx][cy] == startY)) {
        int px = parentX[cx][cy], py = parentY[cx][cy];
        cx = px; cy = py;
    }
    
    *nextX = cx; 
    *nextY = cy;
    return true;
}

// MAIN FUNCTION: Now accepts arguments from the terminal!
int main(int argc, char *argv[]) {
    initMaps();
    
    int robotX = 0, robotY = 0;
    
    // Default goal (Kitchen) if no arguments are provided
    int goalX = 8, goalY = 8; 

    // THE BRIDGE: If Python sends 2 coordinates, override the default
    if (argc == 3) {
        goalX = atoi(argv[1]); 
        goalY = atoi(argv[2]); 
    }

    printf(">> TARGET ACQUIRED: Navigating to X:%d, Y:%d <<\n", goalX, goalY);
    Sleep(1500); 

    // The SLAM Engine Loop
    while (!(robotX == goalX && robotY == goalY)) {
        scanEnvironment(robotX, robotY); 
        printMap(robotX, robotY, goalX, goalY); 

        int nextX, nextY;
        if (calculateNextStep(robotX, robotY, goalX, goalY, &nextX, &nextY)) {
            robotX = nextX; 
            robotY = nextY; 
        } else {
            printf("\n>> FATAL ERROR: Robot is trapped! No path to goal exists.\n");
            break;
        }
        
        Sleep(400); 
    }

    if (robotX == goalX && robotY == goalY) {
        scanEnvironment(robotX, robotY);
        printMap(robotX, robotY, goalX, goalY);
        printf("\n>> TARGET REACHED! SLAM SEQUENCE COMPLETE. <<\n");
    }
    
    return 0;
}