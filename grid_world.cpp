#include <iostream>
#include <string>
#include <vector>
#include <math.h>
#include <stdlib.h> 
#include <time.h>
#include <cmath>
#include <istream>
#include <algorithm>
//g++ -std=c++11 icecream_fan.cpp
int size = 5; //grid size


std::vector<std::vector<int> > grid_layout() {
    std::vector<std::vector<int> > grid_world (size, std::vector<int>(size,0)); //initialize a z*z 0 matrix;
    grid_world[1][1] = 99; //mark obstacle as 1
    grid_world[1][2] = 99;
    grid_world[3][1] = 99;
    grid_world[3][2] = 99;

    grid_world[0][4] = 88; //mark wall as 2
    grid_world[1][4] = 88;
    grid_world[2][4] = 88;
    grid_world[3][4] = 88;
    grid_world[4][4] = 88;

    grid_world[4][2] = 2;//mark icecream shop
    grid_world[2][2] = 2;

    grid_world[0][2] = 1; //mark robot

    return grid_world;
}

void print_grid(const std::vector<std::vector<int> > &grid) {
    for(int i = 0; i < size; i++) {
        for(int j = 0; j < size; j++) {
            if(grid[i][j] == 99) {
                std::cout << " X ";
            } else if (grid[i][j] == 88) {
                std::cout << " W ";
            } else if (grid[i][j] == 2) {
                std::cout << " I ";
            } else if (grid[i][j] == 1) { 
                std::cout << " R ";
            } else {
                std::cout << " 0 ";
            }
        }
        std::cout<<std::endl;
    }
}

int calculate_distance(int i, int j) {
    if(i == 4 && j == 2) {
        return 0;
    }

    if(i == 2 && j == 2) {
        return 0;
    }
    float ds = sqrt(pow((i-4),2)+pow((j-2),2));
    float dd = sqrt(pow((i-2),2)+pow((j-2),2));
    float h = 2/(1/ds + 1/dd);
    int h_up = ceil(h);
    int h_down = floor(h);

    float p_ceil = 1 - (h_up - h);
    //float p_floor = h_up -h;

    bool ceil = ((float) rand() / (RAND_MAX)) < p_ceil;
    if(ceil == true) {
        return h_up;
    } else {
        return h_down;
    }
}


std::vector<std::vector<int> > observation_grid(const std::vector<std::vector<int> > &grid) {
    std::vector<std::vector<int> > observ_map (size, std::vector<int>(size,0));
    for(int i = 0; i < size; i++) {
        for(int j = 0; j < size; j++) {
            if(grid[i][j] < 3) {
                int h_val = calculate_distance(i,j); 
                observ_map[i][j] = h_val;
            } else {
                observ_map[i][j] = 9; //make obstacle as 9;
            }
        }
    }
    return observ_map;
}

void print_observ_map(const std::vector<std::vector<int> > ob_map) {
    for(int i = 0; i < size; i++) {
        for(int j = 0; j < size; j++) {
            std::cout << " " + std::to_string(ob_map[i][j]) + " ";
        }
        std::cout<<std::endl;
    }
}

std::vector<int> find_robot_position(std::vector<std::vector<int> > &grid) {
    std::vector<int> robot_pos;
    for(int i = 0; i < size; i++) {
        for(int j = 0; j < size; j++) {
            if(grid[i][j] == 1) {
                robot_pos.push_back(i);
                robot_pos.push_back(j);
                break;
            }
        }
    }
    return robot_pos;
}

void move_robot(std::string input_command, std::vector<std::vector<int> > &grid) {
    std::vector<int> robot_pos = find_robot_position(grid);
    int row = robot_pos[0];
    int prev_row = row;
    int column = robot_pos[1];
    int prev_column = column;

    grid[row][column] = 0;

    if(input_command == "w") {
        row = row - 1;
    } else if(input_command == "s") {
        row = row + 1;
    } else if(input_command == "a") {
        column = column -1;
    } else if (input_command == "d") {
        column = column +1;
    } else {
        row = row;
        column = column;
    }

    if(row < 0) {
        row = 0;
    } else if ( row > (size - 1)) {
        row = size - 1;
    }

    if(column< 0) {
        column = 0;
    } else if ( column > (size - 1)) {
        column = column - 1;
    }

    if(grid[row][column] > 3) {
        row = prev_row;
        column = prev_column;
    }

    grid[row][column] = 1;
}

struct InputCommand
{
    std::string inputstring;

    /*void InputCheck(std::string &input) {
        if(input != "w" || input != "a" || input !="s" || input !="d" || input !="q") {
            input = "";
        }
    }*/

    int random_value() {
        return rand() % 3;
    }

    std::string GetInput() {
        std::vector<std::string> command_list = {"w", "a", "s", "d", ""};
        std::cin >> inputstring;
        //InputCheck(inputstring);
        std::cin.clear();
        /*float pe = 0.1;
        bool error_or_not = ((float) rand() / (RAND_MAX)) < (1-pe);
        if(error_or_not) {
            command_list.erase(std::remove(command_list.begin(),command_list.end(),inputstring),command_list.end());
            return command_list[random_value()];
        } else {
            
        }*/
        return inputstring;
    }
};


int main() {
    srand(time(0));
    std::vector<std::vector<int> > grid = grid_layout();
    print_grid(grid);
    std::cout << std::endl;
    std::vector<std::vector<int> > observ_map = observation_grid(grid);
    print_observ_map(observ_map);
    InputCommand input_command;
    std::string input = "";
    while(input != "q") {
        input = input_command.GetInput();
        move_robot(input, grid);
        std::cout << std::endl;
        print_grid(grid);
        std::cout << std::endl;
        print_observ_map(observ_map);
    }
    return 0;
}
