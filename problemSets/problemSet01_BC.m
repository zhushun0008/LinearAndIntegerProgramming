%% ProblemSet01_A
foods = {
    'Rice';
    'Quinoa';
    'Tortilla';
    'Lentils'
    'Broccoli'};

Nutrients ={
    'Carbohydrates';
    'Protein';
    'Fat'};

FoodNutrientMatrix = [
    53, 4.4, 0.4; 
    40, 8, 3.6;
    12, 3, 2;
    53, 12, 0.9;
    6, 1.9, 0.3 ];
NutrientFoodMatrix = FoodNutrientMatrix';

% Column form of cost for each food per unit
Cost = [
    0.5
    0.9
    0.1
    0.6
    0.4];

% Define Column form for lower boundry and upper boundry of the amount of 
% nutrients 
nutrientsLowerBoundry = [
    100
    12
    0 ];
nutrientsUpperBoundry = [
    1000
    100
    100 ];

A_big = [
    NutrientFoodMatrix 
    -NutrientFoodMatrix 
    -eye(length(Cost)) 
    ];
b_big = [
    nutrientsUpperBoundry
    -nutrientsLowerBoundry
    zeros(length(Cost),1)
    ];
Sol = linprog(Cost, A_big,b_big);

% Find indices for food we need to take
I = find(Sol> 1e-6);
for i = 1 : length(I)
    disp(foods{I(i)})
end

% Extra constrained matrix for question 06
extraA = bsxfun(@minus, diag([0.5 0.9 0.1 0.6 0.4]), 0.6 * [0.5, 0.9, 0.1, 0.6, 0.4]); 
extrab = zeros(length(Cost),1);
A_big = [
    A_big
    extraA
    ];
b_big = [
    b_big
    extrab
    ];

Sol2 = linprog(Cost, A_big,b_big);
%%