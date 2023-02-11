/*  Author: Charif Bahloul
    Program Description: A 3-part (+2 bonus) adventure game that tests students on their mathematical skills (gr. 10 level) using randomly generated questions while also being fun-to-play. This program incorporates all of the major programming concepts from the course in order to demonstrate my understanding of, and ability to work with, these concepts.
    Date Created: March 10th, 2022
    Date Modified: June 23rd, 2022

    Replit Link: https://replit.com/join/ikxyklboil-charifb
*/

// =================== Preprocessor Commands ==========================
#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <stdlib.h>
#include <unistd.h>
using namespace std;

// ============================= Structures ===========================
struct Hero
{
    int pointsGoal;
    int ePoints; // Game currency.

    int health;
    int damage;
};

struct Enemy
{
    int health;
    int chanceOfNotHitting;
    string name;
    string attackType;
};

struct Quadratic
{
    int a;
    int b;
    int c;
};

struct Linear
{
    int yCoeff;
    int y;
    int m;
    int x;
    int b;
};

// ===================  Function Prototypes  ==========================
int menuSystem();
void main_game_loop(Hero);

void showInstructions(Hero);
void sleepAndClear();
bool checkHealthAndPoints(Hero);
string capitalizeName(string);

int choicesMenu(string, Hero);
void upgrade(Hero &);
bool upgradeIntro(Hero);
int upgradeHealth(Hero);
int upgradeDamage(Hero);
void showFinalStats(Hero);

void runAway(Enemy, Hero &);
void befriend(Enemy, string, Hero &);
void friendshipDeterminer(Enemy, int, Hero &);

void userHit(Enemy &, float, string, bool, Hero);
void enemyHit(Enemy, Hero &);

void enemyDied(Enemy, Hero &);
void showCurrentAdvInstructions(bool);
int userAttackDamageCalculator(int, float, int);

void firstAdventure(Hero &);
void fightWolf(Enemy &, Hero &);
int askUserQuestion1(float &, int, int);
int hitAlgorithm1(int, int, Hero);

void secondAdventure(Hero &);
void fightScorpion(Enemy &, Hero &);
void askUserQuestion2(float &, string, int &, int &);
void quadEquationGenerator(Quadratic &, float &, float &);
string quadEquationConcatenator(Quadratic);
int hitAlgorithm2(int, Quadratic, Hero);

void thirdAdventure(Hero &);
void fightShark(Enemy &, Hero &);
void askUserQuestion3(float &, string, string, int &, int &);
void linearEquationGenerator(Linear &, Linear &);
string linearEquationConcatenator(Linear);
int hitAlgorithm3(int, int, Hero);

void memoryGameLoop(Hero &);
bool askQuestion(int[], int, int &, Hero &);
void showNewNumber(int[], int);
void askForNumber(int[], int &, int);

void battleshipGameLoop(Hero &);
void wonGame(char [7][7], char [7][7], Hero &);
void lostGame(char [7][7], char [7][7], Hero &);

void askAllShipPlacement(char[7][7]);
void placeShipComplete(int, char, string, char[7][7]);

void getUserCoords(int &, int &);
char askUserBattleship(string);
char getOrientation(int, int, char[7][7], int);

void printGrid(char[7][7], string);
void printBotGrid(char[7][7], string);

bool testPlaceShipInGrid(int, int, char, char[7][7], int);
void placeShipInGrid(int, int, char, char[7][7], int, char);

void generateAllRandomShips(char[7][7]);
void generateRandomShip(int, char, string, char[7][7]);
void generateRandomCoords(int &, int &);

void userTurnBattleship(char[7][7], char[7][7]);
void botsTurnBattleship(char[7][7], char[7][7]);
bool isGameOverBattleship(char[7][7]);
int calcPointsBattleship(char[7][7]);

// ===================  Function Definitions  ==========================
int main()
{
    srand(time(NULL)); // To generate a random seed. Note that if you are testing the code, don't comment lines marked as "For testing only".
    int choice = 0;

    Hero userChar;
    userChar.ePoints = 30;

    system("clear");
    cout << "Welcome to Alphadventures.\n\n";

    while (choice != 4)
    {
        choice = menuSystem();

        if (choice == 1) // Depending on what level you want to play at, have respective point goals.
        {
            userChar.pointsGoal = 42;
        }
        else if (choice == 2)
        {
            userChar.pointsGoal = 45;
        }
        else if (choice == 3)
        {
            userChar.pointsGoal = 50;
        }
        else if (choice == 4)
        {
            return 0;
        }
        
        // Notice how references aren't used for userChar so that we don't have to reset it if user replays.
        main_game_loop(userChar); 
    }
    
    return 0;
}

int menuSystem()
{
    /// Returns the user's choice of difficulty.
    int choice = 0;
    do
    {
        cout << "What difficulty would you like to try the game on?\n";
        cout << "1) Easy.\n";
        cout << "2) Medium.\n";
        cout << "3) Hard.\n";
        cout << "4) Quit.\n";
        cin >> choice;

        if (choice < 1 or choice > 4)
        {
            cout << "Invalid input. Please try again.\n\n";
        }
    } while (choice < 1 or choice > 4);

    return choice;
}

void main_game_loop(Hero userChar)
{
    /// This is the loop that goes through all of the adventures.
    
    userChar.health = 0; // Resetting for multiple plays.
    userChar.damage = 0;

    showInstructions(userChar);

    upgrade(userChar);
    firstAdventure(userChar);
    if (checkHealthAndPoints(userChar))
    {
        return;
    }

    upgrade(userChar);
    secondAdventure(userChar);
    if (checkHealthAndPoints(userChar))
    {
        return;
    }

    upgrade(userChar);
    thirdAdventure(userChar);
    if (checkHealthAndPoints(userChar))
    {
        return;
    }

    memoryGameLoop(userChar);
    if (checkHealthAndPoints(userChar))
    {
        return;
    }

    battleshipGameLoop(userChar);
    if (checkHealthAndPoints(userChar))
    {
        return;
    }

    // If you still haven't reached the point goal, you lose.
    cout << "EPoints = " << userChar.ePoints << "\n";
    cout << "Health = " << userChar.health << "\n";
    cout << "YOU LOSE.\n\n\n";

    return;
}

// ===============================================================================
void showInstructions(Hero userChar) 
{
    /// Shows the player an outline of the game and instructions on what they can do.
    cout << "\nTo win, you need to get to " << userChar.pointsGoal << " EPoints."; // Very clear instructions given to ensure first-time players know how to manage their EPoints.
    cout << "\nIf your health dips to 0, you lose. If your ePoints dip to less than 0, you lose.";
    cout << "\nYou will participate in 3 adventures and 2 bonus (and fun)  games.";
    cout << "\n1) Running away. You immediately lose 15 ePoints.";
    cout << "\n2) Befriend. The more ePoints you give as a present, the greater the chance you get away. Otherwise, you lose 25 ePoints.";
    cout << "\n3) Fight. ***RECOMMENDED*** You fight the enemy. If you win, you get 25 ePoints. If you die, you lose.";
    cout << "\nAt the end, there will be 2 bonus games to increase the number of points you have: A bonus memory game and battleship against a bot. In both of these games, you don't need health or damage so plan accordingly.";

    string extraVar = "";
    cout << "\nPress any letter to continue when you're finished reading: ";
    cin >> extraVar;

    system("clear");
    return;
}

void sleepAndClear()
{
    /// Sleeps for 2 seconds and then clears the console.
    sleep(2);
    system("clear");
    return;
}

bool checkHealthAndPoints(Hero userChar)
{ 
    /// If true is returned, means game is complete (i.e. we've reached a win or loss). If false is returned, means game is incomplete. Checks ePoints and health.
    if (userChar.ePoints >= userChar.pointsGoal)
    {
        cout << "EPoints = " << userChar.ePoints << "\n";
        cout << "Health = " << userChar.health << "\n";
        cout << "YOU WIN!\n\n\n";
        return true;
    }

    if (userChar.health <= 0 or userChar.ePoints < 0)
    {
        cout << "EPoints = " << userChar.ePoints << "\n";
        cout << "Health = " << userChar.health << "\n";
        cout << "YOU LOSE.\n\n\n";
        return true;
    }
    return false;
}

string capitalizeName(string name)
{
    /// Returns a string with the first letter capitalized.
    name[0] += 32; // Since a=97 and A=65 (ascii), 97-65=32.
    return name;
}

// ===============================================================================
int choicesMenu(string context, Hero userChar)
{ 
    /// Returns the user's choice to run, befriend or fight the enemy.
    int choice = 0;
    do
    {
        cout << context << " What do you do? \n";
        cout << "1) Run.\n";
        cout << "2) Befriend.\n";
        cout << "3) Fight.\n";
        cin >> choice;

        if (choice < 1 or choice > 3) 
        {
            cout << "Invalid choice. Please try again.\n";
        }
        else if (choice == 1 and userChar.ePoints < 15) // Ensure that the choice is possible with the number of epoints you have.
        {
            cout << "EPoints= " << userChar.ePoints << "\n";
            cout << "You don't have enough EPoints (15 ePoints) to run away. Try again.\n";
        }
        else if (choice == 2 and userChar.ePoints < 25)
        {
            cout << "EPoints= " << userChar.ePoints << "\n";
            cout << "You don't have enough EPoints (25 ePoints for collateral if you fail) to attempt to befriend.\n";
        }
    } while (choice < 1 or choice > 3 or (choice == 1 and userChar.ePoints < 15) or (choice == 2 and userChar.ePoints < 25));
    
    return choice;
}

void upgrade(Hero &userChar)
{
    /// Contains calls to functions that let the user upgrade their health and damage.
    int ePointsAtEnterance = userChar.ePoints;
    int userHealthAtEnterance = userChar.health;
    int userDamageAtEnterance = userChar.damage;

    if (upgradeIntro(userChar)) // Can't upgrade due to lack of ePoints.
    {
        return;
    }

    int increaseHealth = upgradeHealth(userChar);
    userChar.ePoints -= increaseHealth;
    userChar.health += increaseHealth;

    int increaseDamage = upgradeDamage(userChar);
    userChar.ePoints -= increaseDamage;
    userChar.damage += increaseDamage;

    showFinalStats(userChar);
    sleepAndClear();
    return;
}

bool upgradeIntro(Hero userChar)
{
    /// Returns true if the user doesn't have enough points to upgrade.
    cout << "Upgrade Menu- Goal: " << userChar.pointsGoal << "\n"; // Goal is stated so that user can plan accordingly.

    if (userChar.ePoints == 0)
    {
        cout << "EPoints= " << userChar.ePoints << " You don't have any EPoints so you can't upgrade.\n";
        return true; // You don't have ePoints.
    }

    return false; // If you have ePoints.
}

int upgradeHealth(Hero userChar)
{
    /// Returns the amount the user wants to add to their health.
    int increaseHealth = 0;
    do // Upgrade health.
    {
        cout << "EPoints= " << userChar.ePoints << "  Current health= " << userChar.health << "  Health: ";
        cin >> increaseHealth;
            
        if (increaseHealth < 0) // So that they can't trade back ePoints at the end and win.
        {
            cout << "Invalid input. Please try again.\n";
        }
        else if (increaseHealth > userChar.ePoints) // You can't have negative ePoints.
        {
            cout << "You don't have enough ePoints to upgrade. Please try again.\n";
        }
        else if (userChar.health + increaseHealth <= 0) // Since you are upgrading the first time without any health, this can happen. To keep true to the rule of health > 0.
        {
            cout << "You must have positive health.\n";
        }
    } while (increaseHealth > userChar.ePoints or increaseHealth < 0 or userChar.health + increaseHealth <= 0);

    return increaseHealth;
}

int upgradeDamage(Hero userChar)
{
    /// Returns the amount the user wants to add to their damage.
    int increaseDamage = 0;

    do // Upgrade damage.
    {
        cout << "EPoints= " << userChar.ePoints << "  Current damage= " << userChar.damage << "  Damage: ";
        cin >> increaseDamage;
        if (increaseDamage < 0) // Can't trade back damage at the end.
        {
            cout << "Invalid input. Please try again.\n";
        }
        else if (increaseDamage > userChar.ePoints) // You can't have negative ePoints.
        {
            cout << "You don't have enough ePoints to upgrade. Please try again.\n";
        }
    } while (increaseDamage > userChar.ePoints or increaseDamage < 0);

    return increaseDamage;
}

void showFinalStats(Hero userChar)
{
    /// Prints the user's characteristics after upgrading.
    cout << "EPoints= " << userChar.ePoints << "  Current health= " << userChar.health << "  Current damage= " << userChar.damage << "\n";
    return;
}

// ===============================================================================
void runAway(Enemy currEnemy, Hero &userChar)
{
    /// Takes out 15 ePoints for running away from the enemy.
    userChar.ePoints -= 15; // Decrease ePoints by 15 to discourage user from running away. Very hard to win if you run away even once.
    cout << "You ran away from the " << currEnemy.name << " and lost 15 EPoints.\n\n";

    return;
}

// ===============================================================================
void befriend(Enemy currEnemy, string fearFactor, Hero &userChar)
{
    /// Asks the user to give a present to the enemy and calculates whether or not the frienship was successful.
    int presentAmount = 0;

    cout << "As you approach the " << currEnemy.name << ", you notice " << fearFactor << ". You can offer it some EPoints to increase the probability that it will like you.";

    do
    {
        cout << "\nHow much do you want to give? ";
        cin >> presentAmount;

        if (presentAmount > userChar.ePoints) // Can't give more than you have.
        {
            cout << "EPoints= " << userChar.ePoints << "\n";
            cout << "You can't give more ePoints than you have. Try again.\n\n";
        }
    } while (presentAmount > userChar.ePoints);

    userChar.ePoints -= presentAmount;
    friendshipDeterminer(currEnemy, presentAmount, userChar);
    return;
}

void friendshipDeterminer(Enemy currEnemy, int presentAmount, Hero &userChar)
{
    /// Calculates whether or not the frienship was successful based on the present given.
    if (presentAmount >= 15)
    { // Greater than or equal to what you'd have given if you ran.
        cout << "Friendship accepted. Never knew you were this good with " << currEnemy.name << ". Wow.\n";
    }
    else // Otherwise, the more you give, the higher the probability that you are befriended and not killed.
    {
        int friendshipAccepted = rand() % (16 - presentAmount); // Probability enemy accepts your friendship request.
        if (friendshipAccepted == 1) // Prints out whether or not friendship was accepted.
        {
            cout << "Friendship accepted. Never knew you were this good with " << currEnemy.name << ". Wow.\n";
        }
        else
        {
            cout << "You approached the " << currEnemy.name << " and the " << currEnemy.name << " tried to " << currEnemy.attackType << " you. You escaped by the skin of your teeth but lost 25 Epoints in the process.\n";
            userChar.ePoints -= 25; // If you are not befriended, you lose 25 ePoints.
        }
    }
            
    return;
}

// ===============================================================================
void userHit(Enemy &currEnemy, float timeTaken, string realAnswer, bool isUserCorrect, Hero userChar)
{
    /// If correct, outputs correct. Else, outputs wrong.
    if (isUserCorrect)
    {

        cout << "CORRECT. Your health: " << userChar.health << "  " << currEnemy.name << "'s Health: " << currEnemy.health << "\n\n";
    }
    else
    {
        cout << "WRONG. The correct answer is: " << realAnswer << " Your health: " << userChar.health << "  " << currEnemy.name << "'s Health: " << currEnemy.health << "\n\n";
    }

    return;
}

void enemyHit(Enemy currEnemy, Hero &userChar)
{ 
    /// Uses enemy chanceOfNotHitting to determine if the enemy landed a blow (2 points damage).
    string enemyNameLower = capitalizeName(currEnemy.name);

    if (rand() % currEnemy.chanceOfNotHitting != 0) // Uses the enemy's chance variable to determine if the user is hit or not and outputs that.
    {
        userChar.health -= 2;
        cout << "The " << enemyNameLower << " " << currEnemy.attackType << " you. Your health: " << userChar.health << "  " << currEnemy.name << "'s Health: " << currEnemy.health << "\n";
    }
    else
    {
        cout << "The " << enemyNameLower << " didn't " << currEnemy.attackType << " you. Your health: " << userChar.health << "  " << currEnemy.name << "'s Health: " << currEnemy.health << "\n";
    }

    return;
}

// ===============================================================================
void enemyDied(Enemy currEnemy, Hero &userChar) 
{
    /// You beat the enemy and got 25 ePoints for that.
    cout << "You beat the " << currEnemy.name << "! CONGRATS! You get 25 EPoints.\n\n";
    userChar.ePoints += 25;

    return;
}

void showCurrentAdvInstructions(bool showInstructions)
{
    /// Gives instructions for the user, sleeps and clears.
    if (showInstructions) 
    {
        cout << "Get ready. Note that the questions are timed and get progressively harder. You'll need a pencil and paper. NO CALCULATORS.\n";
        sleep(2);
    }

    sleep(1);
    system("clear");
    return;
}

int userAttackDamageCalculator(int timeTaken, float maxTime, int userDamage) 
{
    /// Uses a linear algorithm for calculating user damage and returns that.
    return (1 - ((timeTaken / maxTime) / 2.0)) * userDamage;
}

// ===============================================================================
void firstAdventure(Hero &userChar)
{
    /// Contains calls for the first adventure.
    int firstAdventureChoice = choicesMenu("Armed with your weapons, you venture into the mountains. All of a sudden, you encounter a wolf.", userChar);

    Enemy wolf;
    wolf.health = 42;
    wolf.chanceOfNotHitting = 5;
    wolf.name = "Wolf";
    wolf.attackType = "bite";

    if (firstAdventureChoice == 1) // Run, befriend, fight respectively.
    {
        runAway(wolf, userChar);
    }
    else if (firstAdventureChoice == 2)
    {
        befriend(wolf, "how hungry it is", userChar);
    }
    else if (firstAdventureChoice == 3)
    {
        fightWolf(wolf, userChar);
    }

    sleepAndClear();
    return;
}

void fightWolf(Enemy &wolf, Hero &userChar)
{
    /// Contains game loop for fighting the wolf.
    showCurrentAdvInstructions(true);

    int increment = 0;
    float timeTaken = 0.0;

    while (wolf.health > 0 and userChar.health > 0) // Fighting loop.
    {
        int number1 = rand() % 10 + increment; // Generate factors with increment to make it harder each time.
        int number2 = rand() % 10 + increment;

        int userAnswer = askUserQuestion1(timeTaken, number1, number2);

        bool isUserCorrect = (number1 * number2 == userAnswer);
        if (isUserCorrect)
        {
            wolf.health -= hitAlgorithm1(timeTaken, increment, userChar);
        }

        userHit(wolf, timeTaken, to_string(number1 * number2), isUserCorrect, userChar);

        enemyHit(wolf, userChar);
        increment += 5; // Increase in difficulty.
    }
    if (wolf.health <= 0 and userChar.health > 0) // If the wolf's done, give reward. Otherwise, if health is 0 or less, it'll be identified in checkHealthAndPoints.
    {
        enemyDied(wolf, userChar);
    }
    return;
}

int askUserQuestion1(float &timeTaken, int number1, int number2) 
{
    /// Returns the time taken to answer the question through references and returns the answer the user gave.
    int startTime = time(NULL);
    int userAnswer = 0;

    // cout << "Answer: " << number1*number2 << "\n"; // For testing only.
    cout << "What is " << number1 << "*" << number2 << " ? ";
    cin >> userAnswer;

    timeTaken = time(NULL) - startTime; // Time taken in seconds.
    return userAnswer;
}

int hitAlgorithm1(int timeTaken, int increment, Hero userChar)
{
    /// Returns the damage given by the user.
    float maxTime = 0.0;
    int userAttackDamage = 0;
    if (increment < 10) // Depending on how big the number is (using increment), different time range.
    {
        maxTime = 2;
    }
    else if (increment <= 20)
    {
        maxTime = 10;
    }
    else if (increment <= 40)
    {
        maxTime = 15;
    }
    else
    {
        maxTime = 25;
    }

    if (timeTaken >= maxTime * 1.5) // Doesn't fit the algorithm below. Separate algorithm.
    {
        userAttackDamage = maxTime / 3 + 1;
    }
    else
    {
        userAttackDamage = userAttackDamageCalculator(timeTaken, maxTime, userChar.damage);
    }
    return userAttackDamage;
}

// ===============================================================================
void secondAdventure(Hero &userChar)
{
    /// Contains calls for the second adventure.
    int secondAdventureChoice = choicesMenu("Following your fierce encounter with the wolf, you continue your trek into the desert. As you're walking, you notice a scorpion right beside your foot.", userChar);

    Enemy scorpion;
    scorpion.health = 42;
    scorpion.chanceOfNotHitting = 4;
    scorpion.name = "Scorpion";
    scorpion.attackType = "stung";

    if (secondAdventureChoice == 1) // Run, befriend or fight respectively.
    {
        runAway(scorpion, userChar);
    }
    else if (secondAdventureChoice == 2)
    {
        befriend(scorpion, "how its pincers are gleaming with poison", userChar);
    }
    else if (secondAdventureChoice == 3)
    {
        fightScorpion(scorpion, userChar);
    }

    sleepAndClear();
    return;
}

void fightScorpion(Enemy &scorpion, Hero &userChar)
{
    /// Contains the game loop for the second adventure.
    showCurrentAdvInstructions(false);

    while (scorpion.health > 0 and userChar.health > 0)
    {
        Quadratic equation; // Initialize variables to generate quad. equation.

        float realRoot1 = 0;
        float realRoot2 = 0;

        int userRoot1 = 0;
        int userRoot2 = 0;

        float timeTaken = 0.0;

        quadEquationGenerator(equation, realRoot1, realRoot2);
        string quadEquation = quadEquationConcatenator(equation);

        // cout << "Answer: " << realRoot1 << "  " << realRoot2 << "\n"; // For testing only.
        askUserQuestion2(timeTaken, quadEquation, userRoot1, userRoot2);
        bool isUserCorrect = ((userRoot1 == realRoot1 and userRoot2 == realRoot2) or (userRoot1 == realRoot2 and userRoot2 == realRoot1)); // Ok if written in reverse.

        if (isUserCorrect)
        {
            scorpion.health -= hitAlgorithm2(timeTaken, equation, userChar);
        }

        userHit(scorpion, timeTaken, to_string(realRoot1) + " & " + to_string(realRoot2), isUserCorrect, userChar);
        enemyHit(scorpion, userChar);
    }
    if (scorpion.health <= 0 and userChar.health > 0)
    {
        enemyDied(scorpion, userChar);
    }

    return;
}

void askUserQuestion2(float &timeTaken, string quadEquation, int &userRoot1, int &userRoot2)
{ 
    /// Returns the time taken to answer the question through references and returns the answer the user gave.
    int startTime = time(NULL);

    cout << "Given the following quadratic equation: \n"
         << quadEquation << "\n";

    cout << "What is the first zero: ";
    cin >> userRoot1;
    cout << "What is the second zero (if there's only 1 zero, type again): ";
    cin >> userRoot2;

    timeTaken = time(NULL) - startTime; // Time taken in seconds.
    return;
}

void quadEquationGenerator(Quadratic &equation, float &realRoot1, float &realRoot2)
{
    /// Generates a quadratic equation with integer a, b and c variables.
    do // Make sure it's an integer because floats have precision error when comparing to what the user wrote.
    {
        do
        {
            equation.a = rand() % 21 - 10; // -10 -> 10 inclusive.

            realRoot1 = rand() % 31 - 15;
            realRoot2 = rand() % 31 - 15;
        } while (equation.a == 0 or realRoot1 == 0 or realRoot2 == 0);
        // Has to be a quadratic. Can't divide by 2a = 2*0 = 0 in quad. formula.

        equation.b = -1 * equation.a * (realRoot1 + realRoot2);
        equation.c = equation.a * realRoot1 * realRoot2;

    } while (equation.b > 100 or equation.c > 100);

    return;
}

string quadEquationConcatenator(Quadratic equation)
{ 
    /// Returns a concatenated string to display for the quadratic equation.
    string quadDisplay = "";

    if (equation.a == 1) // Displaying the a-variable appropriately.
    {
        quadDisplay += "x^2 ";
    }
    else if (equation.a == -1)
    {
        quadDisplay += "-x^2 ";
    }
    else if (equation.a != 0)
    {
        // Converting equation.a to a string as the coefficient. Note that 0 isn't a case because it would have been stopped in quadEquationGenerator.
        quadDisplay += to_string(equation.a) + "x^2 "; 
    }

    if (equation.b == 1) // Displaying the b-variable appropriately.
    {
        quadDisplay += "+x ";
    }
    else if (equation.b == -1)
    {
        quadDisplay += "-x ";
    }
    else if (equation.b > 0)
    {
        quadDisplay += "+ " + to_string(equation.b) + "x ";
    }
    else if (equation.b < 0) // If b is 0, it's skipped.
    {
        quadDisplay += to_string(equation.b) + "x ";
    }

    if (equation.c > 0) // Displaying the c-variable appropriately.
    {
        quadDisplay += "+ " + to_string(equation.c);
    }
    else if (equation.c < 0)
    {
        quadDisplay += to_string(equation.c);
    }
    return quadDisplay;
}

int hitAlgorithm2(int timeTaken, Quadratic equation, Hero userChar)
{
    /// Returns the damage given by the user.
    float maxTime = 0.0;
    int userAttackDamage = 0;

    if (equation.b == 0 or equation.c == 0) // Depending on the difficulty of the question (e.g. if a != 1), changes maxTime.
    {
        maxTime = 7.0;
    }
    else if (equation.a == 1)
    {
        maxTime = 10.0;
    }
    else
    {
        maxTime = 23.0;
    }

    if (timeTaken >= maxTime * 1.5)
    {
        userAttackDamage = maxTime / 3 + 1;
    }
    else
    {
        userAttackDamage = userAttackDamageCalculator(timeTaken, maxTime, userChar.damage); // Note that if you get exactly maxTime, you get your normal damage (userChar.damage). Less gives you less damage and more gives you more.
    }
    return userAttackDamage;
}

// ===============================================================================
void thirdAdventure(Hero &userChar)
{
    /// Contains function calls for the third adventure.
    int thirdAdventureChoice = choicesMenu("After winning the battle with the scorpion, you continue into the ocean. As you're sailing, a shark slams into your boat.", userChar);

    Enemy shark;
    shark.health = 42;
    shark.chanceOfNotHitting = 4;
    shark.name = "Shark";
    shark.attackType = "bite";

    if (thirdAdventureChoice == 1) // Which action was chosen?
    {
        runAway(shark, userChar);
    }
    else if (thirdAdventureChoice == 2)
    {
        befriend(shark, "how hungry it is", userChar);
    }
    else if (thirdAdventureChoice == 3)
    {
        fightShark(shark, userChar);
    }

    sleepAndClear();
    return;
}

void fightShark(Enemy &shark, Hero &userChar)
{
    /// Contains game loop for fighting the shark.
    showCurrentAdvInstructions(false);

    while (shark.health > 0 and userChar.health > 0) // Game loop.
    {
        Linear equation1; // Initializing system of equations.
        Linear equation2;

        linearEquationGenerator(equation1, equation2); // Generate system of equations.
        string linearEquation1 = linearEquationConcatenator(equation1);
        string linearEquation2 = linearEquationConcatenator(equation2);

        int startTime = time(NULL);
        int userX = 0;
        int userY = 0;
        float timeTaken = 0.0;

        // cout << "Answer: " << equation1.x << "  " << equation1.y << "\n"; // For testing only.
        askUserQuestion3(timeTaken, linearEquation1, linearEquation2, userX, userY);
        bool isUserCorrect = (userX == equation1.x and userY == equation1.y);

        if (isUserCorrect)
        {
            // Second input is an approximation of how easy the question is (bigger numbers = harder problem).
            shark.health -= hitAlgorithm3(timeTaken, (abs(equation1.x) + abs(equation1.y)) * (abs(equation1.yCoeff) + abs(equation2.yCoeff) + abs(equation1.m) + abs(equation2.m) + abs(equation1.b) + abs(equation2.b)), userChar); 
        }
        userHit(shark, timeTaken, "x= " + to_string(equation1.x) + " & y= " + to_string(equation1.y), isUserCorrect, userChar);

        enemyHit(shark, userChar);
    }
    if (shark.health <= 0 and userChar.health > 0) // You killed the enemy.
    {
        enemyDied(shark, userChar);
    }
    return;
}

void askUserQuestion3(float &timeTaken, string linearEquation1, string linearEquation2, int &userX, int &userY)
{
    /// Returns the time taken to answer the question through references and returns the answer the user gave.
    int startTime = time(NULL);

    cout << "Given the system of equations: \n"
         << linearEquation1 << "\n"
         << linearEquation2 << "\n";
            
    cout << "What is the value of x: ";
    cin >> userX;
    cout << "What is the value of y: ";
    cin >> userY;

    timeTaken = time(NULL) - startTime; // Time taken in seconds.
    return;
}

void linearEquationGenerator(Linear &equation1, Linear &equation2)
{
    /// Generates 2 linear equations with integer variables and other restrictions. 
    do
    { 
        equation1.x = rand() % 31 - 15; // -15 --> 15 (Inclusive). 
        equation1.y = rand() % 31 - 15; // -15 --> 15 (Inclusive).

        equation1.yCoeff = rand() % 11 - 5; // -5 --> 5 (Inclusive).
        equation2.yCoeff = rand() % 11 - 5; // -5 --> 5 (Inclusive).

        equation1.m = rand() % 21 - 10; // -10 --> 10 (Inclusive).
        equation2.m = rand() % 21 - 10; // -10 --> 10 (Inclusive).

        equation1.b = equation1.yCoeff * equation1.y - equation1.m * equation1.x;
        equation2.b = equation2.yCoeff * equation2.y - equation2.m * equation2.x;

    } while (equation1.m == 0 or equation2.b == 0 or equation1.yCoeff == 0 or equation2.yCoeff == 0 or equation1.x == 0 or equation1.y == 0 or equation1.yCoeff == equation2.yCoeff or equation1.b > 100 or equation2.b > 100); // Don't want the same equation and don't want 0 values to keep the time it takes to solve consistent. Also don't want huge numbers.

    equation2.x = equation1.x; // Both equations have the same x & y because they are a system of equations.
    equation2.y = equation1.y;

    return;
}

string linearEquationConcatenator(Linear equation)
{
    /// Generates a string to display the linear equation nicely.
    string linearEquation = "";

    if (equation.yCoeff == -1) // Same system as quadEquationConcatenator (refer to those comments). Different variables though.
    {
        linearEquation += "-y = ";
    }
    else if (equation.yCoeff == 1)
    {
        linearEquation += "y = ";
    }
    else
    {
        linearEquation += to_string(equation.yCoeff) + "y = "; // to_string makes the int into a string.
    }

    if (equation.m == 1)
    {
        linearEquation += "x ";
    }
    else if (equation.m == -1)
    {
        linearEquation += "-x ";
    }
    else if (equation.m != 0)
    {
        linearEquation += to_string(equation.m) + "x ";
    }

    if (equation.b > 0)
    {
        linearEquation += "+ " + to_string(equation.b);
    }
    else if (equation.b < 0)
    {
        linearEquation += to_string(equation.b);
    }

    return linearEquation;
}

int hitAlgorithm3(int timeTaken, int difficulty, Hero userChar)
{
    /// Returns the user damage.
    float maxTime = 0.0;
    int userAttackDamage = 0;

    if (difficulty < 1000) // Depending on difficulty, different expected mex. time.
    {
        maxTime = 20.0;
    }
    else if (difficulty < 2000)
    {
        maxTime = 25.0;
    }
    else
    {
        maxTime = 30.0;
    }

    if (timeTaken >= maxTime * 1.5) // Not compatible. 
    {
        userAttackDamage = maxTime / 3 + 1;
    }
    else
    {
        userAttackDamage = userAttackDamageCalculator(timeTaken, maxTime, userChar.damage);
    }
    return userAttackDamage;
}
    
// ===============================================================================
void memoryGameLoop(Hero &userChar)
{
    /// Game loop for memory game.
    cout << "Welcome to the memory game. You'll be given a number and then have to repeat all the numbers up to that number back. Current ePoints = " << userChar.ePoints << "\n" << "You need " << userChar.pointsGoal - userChar.ePoints << " more ePoints.\n";
    sleep(4);

    int memoryNumbers[20] = {}; // If you can remember more than 20 nums, you're cheating.
    int numStrikes = 0;

    for (int i = 0; i < 20; i++) // Iterates through 20 rounds.
    {
        if (askQuestion(memoryNumbers, i, numStrikes, userChar)) // Game is over. Return to mainGameLoop.
        {
            return;
        }
    }

    cout << "Congratulations, you beat the bonus game. Your score: 20\n"; // 20 points max. At that point, you're probably cheating.
    userChar.ePoints += 20;
            
    sleepAndClear();
    return;
}

bool askQuestion(int memoryNumbers[], int currIndex, int &numStrikes, Hero &userChar)
{
    /// Returns true to indicate the game is finishe. Asks user for all numbers up to and including the currIndex.
    memoryNumbers[currIndex] = rand() % 9 + 1; // Generate the new number. 1-9.
    showNewNumber(memoryNumbers, currIndex);

    for (int i = 0; i <= currIndex; i++) // Ask for the previous numbers (including that number).
    {
        askForNumber(memoryNumbers, numStrikes, i);

        if (numStrikes == 3) // Allowed 3 strikes.
        {
            cout << "\nYOU LOSE. You have 3 strikes. Your score: " << currIndex << "\n";
            userChar.ePoints += currIndex; // Add points to user's ePoints.
            return true; // To show the game is done.
        }
    }

    return false;
}

void showNewNumber(int memoryNumbers[], int currIndex)
{
    /// Shows user new number for 2 seconds and then clears the console.
    sleep(2);
    system("clear");
    cout << "New number: " << memoryNumbers[currIndex] << "\n";

    sleepAndClear();
    return;
}

void askForNumber(int memoryNumbers[], int &numStrikes, int i)
{
    /// Asks for a number and checks if it's the right number. If wrong, adds a strike.
    int userInput = 0;
    cout << "Number " << i + 1 << ": ";

    do
    {
        cin >> userInput;
        if (userInput < 0 or userInput > 9)
        {
            cout << "The number has to be between 0-9 (inclusive).\n";
        }
    } while (userInput < 0 or userInput > 9);

    if (userInput == memoryNumbers[i]) // Check if the number is correct.
    {
        cout << "Correct.\n";
    }
    else
    {
        numStrikes++; // Add a strike.
        cout << "Incorrect. Correct answer: " << memoryNumbers[i] << "     Num. strikes: " << numStrikes << "\n";
    }
    return;
}

// ===============================================================================
void battleshipGameLoop(Hero &userChar)
{
    /// Game loop for battleship game.
    sleepAndClear();
    cout << "Welcome to Battleship. You'll be playing against the Alpha bot. Current ePoints = " << userChar.ePoints << "\n" << "You need " << userChar.pointsGoal - userChar.ePoints << " more ePoints.\n"; // Introduce game and objective.
            
    char grid1[7][7] = {{'~', '~', '~', '~', '~', '~', '~'}, // For user.
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'}};

    char grid2[7][7] = {{'~', '~', '~', '~', '~', '~', '~'}, // For bot.
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'},
                        {'~', '~', '~', '~', '~', '~', '~'}};

    // Carrier (5 spaces) = "c", Battleship (4) = "b", Cruiser (3) = "r", Submarine (3) = "s", and Destroyer (2) = "d", Empty = "~", hit = "#". If a ship is hit, that coordinate's letter becomes upper-case.

    askAllShipPlacement(grid1); // User can make their own grid or randomize.
    generateAllRandomShips(grid2); // Reandomized grid for bot.

    while (true) // Will return once the game is won or lost.
    {
        userTurnBattleship(grid1, grid2);
        if (isGameOverBattleship(grid2)) // Check if second grid is done. That would mean the user has won.
        {
            wonGame(grid1, grid2, userChar);
            return;
        }

        botsTurnBattleship(grid1, grid2);
        if (isGameOverBattleship(grid1))  // Check if first grid is done. That would mean the bot has won.
        {
            lostGame(grid1, grid2, userChar);
            return;
        }
    }
}

void wonGame(char grid1[7][7], char grid2[7][7], Hero &userChar)
{ 
    /// Show both grids and points gained.
    printGrid(grid1, "Your Grid.");
    printGrid(grid2, "Bot's Grid.");

    int points = calcPointsBattleship(grid1);
    cout << "You win. Points gained = " << points << ".\n";
    userChar.ePoints += points; // Adding points to user's ePoints.

    return;
}

void lostGame(char grid1[7][7], char grid2[7][7], Hero &userChar)
{ 
    /// Show both grids and lose message.
    printGrid(grid1, "Your Grid.");
    printGrid(grid2, "Bot's Grid.");
    cout << "You lose. Points gained = 0.\n"; // If you lose, you don't get any points.

    return;
}

// ===============================================================================
void askAllShipPlacement(char grid[7][7]) 
{   
    /// Asks the user to place ships manually or randomize and calls the respective functions.
    if (askUserBattleship("Pick where you want to put your ships. Do you want to randomize the placement of ships (y/n)? ") == 'y')
    {
        do
        {
            for (int i = 0; i < 7; i++) // Reset the grid.
            {
                for (int l = 0; l < 7; l++)
                {
                    grid[i][l] = '~';
                }
            }

            generateAllRandomShips(grid);
            printGrid(grid, "Your grid.");
        } while (askUserBattleship("Are you satisfied with this random attempt (y/n)? ") == 'n');
    }
    else
    { // Manually place the ships.
        placeShipComplete(5, 'c', "carrier", grid);
        placeShipComplete(4, 'b', "battleship", grid);
        placeShipComplete(3, 'r', "cruiser", grid);
        placeShipComplete(3, 's', "submarine", grid);
        placeShipComplete(2, 'd', "destroyer", grid);
    }

    return;
}

void placeShipComplete(int lengthShip, char shipSymbol, string shipName, char grid[7][7]) 
{
    /// Puts an individual ship on the grid according to the user's input.
    int xCoord = 0;
    int yCoord = 0;
    cout << "Where do you want to put your " << shipName << " (" << lengthShip << " spaces)?\n";

    do
    {
        printGrid(grid, "Your grid.");
        getUserCoords(xCoord, yCoord);
        if (grid[yCoord][xCoord] != '~')
        {
            cout << "The current coordinate is in use.\n";
        }
    } while (grid[yCoord][xCoord] != '~');
    
    char orientation = getOrientation(xCoord, yCoord, grid, lengthShip);
    placeShipInGrid(xCoord, yCoord, orientation, grid, lengthShip, shipSymbol);
    return;
}

// ===============================================================================
void getUserCoords(int &xCoord, int &yCoord) 
{  
    // Gets coordinates from user and makes sure they're valid.
    do
    {
        cout << "X-Coordinate: ";
        cin >> xCoord;
        cout << "Y-Coordinate: ";
        cin >> yCoord;
        if (xCoord < 1 or xCoord > 7 or yCoord < 1 or yCoord > 7)
        {
            cout << "The coordinate is out of bounds. Try again.\n";
        }
    } while (xCoord < 1 or xCoord > 7 or yCoord < 1 or yCoord > 7);

    yCoord = 7 - yCoord; // Convert it into a format for the array. Array start at 0 and go down to 6.
    xCoord --; // Arrays start at 0, not 1.
    
    // cout << "Actual coordinates: " << xCoord << "  " << yCoord << "\n";
    return;
}

char askUserBattleship(string question)
{   
    // Returns a yes or no from the user after printing the question.
    char choice = 'a';
    do
    {
        cout << question;
        cin >> choice;
        if (choice != 'y' and choice != 'n')
        {
            cout << "Invalid input. Try again.\n";
        }
    } while (choice != 'y' and choice != 'n');
    return choice;
}

char getOrientation(int xCoord, int yCoord, char grid[7][7], int lengthShip)
{   
    /// Returns a valid orientation according to the user's input.
    char orientation = 'l';
    bool correctOrientation = true;

    do
    {
        cout << "What orientation should the ship be in? ";
        cin >> orientation;

        if (!testPlaceShipInGrid(xCoord, yCoord, orientation, grid, lengthShip))
        {
            correctOrientation = false; // So that we don't have to recall the function. Efficiency.
            cout << "In this orientation, the ship either goes out of bounds or hits another ship. Try again.\n";
        }
        else if (orientation != 'r' && orientation != 'l' && orientation != 'u' && orientation != 'd')
        {
            cout << "Invalid input. Try again.\n";
            correctOrientation = false;
        }
        else
        {
            correctOrientation = true;
        }

    } while (!correctOrientation);

    system("clear");
    return orientation;
}

// ===============================================================================
void printGrid(char grid[7][7], string prelude)
{   
    /// Prints the complete grid.
    cout << prelude << "\n";

    for (int i = 0; i < 7; i++)
    {
        cout << 7 - i << " ";
        for (int l = 0; l < 7; l++)
        {
            cout << grid[i][l] << " ";
        }
        cout << "\n";
    }
    cout << "  1 2 3 4 5 6 7\n";
    return;
}

void printBotGrid(char grid[7][7], string prelude)
{
    /// Prints opponent's grid when playing (hides answers).
    cout << prelude << "\n";

    for (int i = 0; i < 7; i++)
    {
        cout << 7 - i << " ";
        for (int l = 0; l < 7; l++)
        {
            if (grid[i][l] == 'c' or grid[i][l] == 'b' or grid[i][l] == 'r' or grid[i][l] == 's' or grid[i][l] == 'd') // Ships not guessed.
            {
                cout << "~ ";
            }
            else
            {
                cout << grid[i][l] << " ";
            }
        }
        cout << "\n";
    }

    cout << "  1 2 3 4 5 6 7\n";
    return;
}

// ===============================================================================
bool testPlaceShipInGrid(int xCoord, int yCoord, char orientation, char grid[7][7], int lengthShip)
{   
    /// Returns true if ship can be placed without going out of bounds or hitting another ship.
    for (int i = 0; i < lengthShip; i++)
    {
        if (orientation == 'r')
        {
            if (xCoord + i > 6 or xCoord + i < 0 or grid[yCoord][xCoord + i] != '~')
            {
                return false;
            }
        }
        else if (orientation == 'l')
        {
            if (xCoord - i > 6 or xCoord - i < 0 or grid[yCoord][xCoord - i] != '~')
            {
                return false;
            }
        }
        else if (orientation == 'u')
        {
            if (yCoord - i > 6 or yCoord - i < 0 or grid[yCoord - i][xCoord] != '~')
            {
                return false;
            }
        }
        else if (orientation == 'd')
        {
            if (yCoord + i > 6 or yCoord + i < 0 or grid[yCoord + i][xCoord] != '~')
            {
                return false;
            }
        }
    }
    return true;
}

void placeShipInGrid(int xCoord, int yCoord, char orientation, char grid[7][7], int lengthShip, char shipSymbol)
{   
    /// Places the ship in the grid.
    for (int i = 0; i < lengthShip; i++)
    {
        switch (orientation)
        {
            case 'r':
                grid[yCoord][xCoord + i] = shipSymbol;
                break;
            case 'l':
                grid[yCoord][xCoord - i] = shipSymbol;
                break;
            case 'u':
                grid[yCoord - i][xCoord] = shipSymbol;
                break;
            case 'd':
                grid[yCoord + i][xCoord] = shipSymbol;
                break;
        }
    }
    return;
}

// ===============================================================================
void generateAllRandomShips(char grid[7][7]) 
{
    /// Generates all of the random ships for the grid.
    generateRandomShip(5, 'c', "carrier", grid);
    generateRandomShip(4, 'b', "battleship", grid);
    generateRandomShip(3, 'r', "cruiser", grid);
    generateRandomShip(3, 's', "submarine", grid);
    generateRandomShip(2, 'd', "destroyer", grid);

    return;
}

void generateRandomShip(int lengthShip, char shipSymbol, string shipName, char grid[7][7])
{   
    /// Generates random coordinates and orientations until it finds a valid ship placement.
    int randXCoord = 0;
    int randYCoord = 0;

    int randOrientationNum = 0;
    char orientationArray[4] = {'r', 'l', 'u', 'd'};
    char randOrientation = 'a';

    do
    {
        generateRandomCoords(randXCoord, randYCoord);

        randOrientationNum = rand() % 4;
        randOrientation = orientationArray[randOrientationNum]; // Converts the random orientation number to a letter orientation.

    } while (grid[randYCoord][randXCoord] != '~' || !testPlaceShipInGrid(randXCoord, randYCoord, randOrientation, grid, lengthShip));

    placeShipInGrid(randXCoord, randYCoord, randOrientation, grid, lengthShip, shipSymbol);
    return;
}

void generateRandomCoords(int &randXCoord, int &randYCoord)
{   
    /// Generates random coordinates from 0-6 (x and y-coordintes).
    randXCoord = rand() % 7;
    randYCoord = rand() % 7;
    return;
}

// ===============================================================================
void userTurnBattleship(char grid1[7][7], char grid2[7][7])
{
    /// Shows the user both grids and asks where they want to hit.
    printGrid(grid1, "Your grid (Capital = guessed)."); // Prints both grids once per turn.
    printBotGrid(grid2, "Bot's grid.");

    int xCoord = 0;
    int yCoord = 0;
    char possibleShips[5] = {'c', 'b', 'r', 's', 'd'};

    do
    {
        getUserCoords(xCoord, yCoord);

        // Makes sure you're not double-guessing.
        if (grid2[yCoord][xCoord] < 96 or grid2[yCoord][xCoord] == '#') 
        {
            cout << "Don't double-guess. Try agin.\n";
        }
    } while (grid2[yCoord][xCoord] < 96 or grid2[yCoord][xCoord] == '#'); // Make sure they don't double-guess.

    bool hitShip = false;

    // Checking if you've hit a ship.
    for (int i = 0; i < 5; i++)
    {
        if (grid2[yCoord][xCoord] == possibleShips[i])
        {
            hitShip = true;
        }
    }

    // If you've hit nothing, make it a '#' to indicate that it's a miss.
    if (grid2[yCoord][xCoord] == '~')
    {
        grid2[yCoord][xCoord] = '#';
    }
    else // If you've hit something, make it upper-case.
    {
        grid2[yCoord][xCoord] -= 32;
    }

    if (hitShip)
    {
        cout << "You hit a ship. Look below to see what you hit.\n";
    }
    else
    {
        cout << "You didn't hit a ship.\n";
    }

    return;
}

void botsTurnBattleship(char grid1[7][7], char grid2[7][7])
{
    /// Hits a random coordinate on the player's grid.
    int randXCoord = 0;
    int randYCoord = 0;
            
    do
    {
        generateRandomCoords(randXCoord, randYCoord);
    } while (grid1[randYCoord][randXCoord] < 96 or grid1[randYCoord][randXCoord] == '#'); // Generates a random coordinate but makes sure you're not double guessing.

    if (grid1[randYCoord][randXCoord] == '~') // If it's a miss, mark it as so.
    {
        grid1[randYCoord][randXCoord] = '#';
    }
    else // Otherwise, if it's a hit, make it upper-case.
    {
        grid1[randYCoord][randXCoord] -= 32;
    }

    cout << "The bot hit the coordinates: (" << randXCoord << ", " << randYCoord << ").\n";
    return;
}

bool isGameOverBattleship(char grid[7][7])
{
    /// Returns true if the game is over (all ships sunk).
    char possibleShips[5] = {'c', 'b', 'r', 's', 'd'};
    for (int i = 0; i < 7; i++)
    {
        for (int l = 0; l < 7; l++) // Goes through every coordinate. 2-d array so we need 2 for loops.
        {
            for (int a = 0; a < 5; a++) // Iterates through the 5 types of ships to check if a ship hasn't been hit.
            {
                if (possibleShips[a] == grid[i][l])
                {
                    return false; // If a ship still isn't hit on your opponent's board, the game is still on.
                }
            }
        }
    }
    return true;
}

int calcPointsBattleship(char grid[7][7]) 
{
    /// Returns the difference between the number of coordinate guessed correctly in grid2 (all=17 since you won) and those in grid 1 (how many the bot got).
    int points = 17;
    for (int i = 0; i < 7; i++) // Goes through each coordinate in the grid.
    {
        for (int l = 0; l < 7; l++)
        {
            if (grid[i][l] < 96 and grid[i][l] != '~' and grid[i][l] != '#')
            {
                points--; // Difference between user who won and bot becomes lower.
            }
        }
    }
    return points;
}
