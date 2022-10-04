[![Codacy Badge](https://app.codacy.com/project/badge/Grade/cfd443ea5bb04867ac9c898c229650b6)](https://www.codacy.com/gh/galyfray/CVRP/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=galyfray/CVRP&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/cfd443ea5bb04867ac9c898c229650b6)](https://www.codacy.com/gh/galyfray/CVRP/dashboard?utm_source=github.com&utm_medium=referral&utm_content=galyfray/CVRP&utm_campaign=Badge_Coverage)
# CVRP


The vehicle routing problem (VRP) is a combinatorial optimization and integer programming problem which asks “What is the optimal set of routes for a fleet of vehicles to traverse in order to deliver to a given set of customers?”  The objective of the VRP is to minimize the total route cost. For the VRP, we consider a single depot, k vehicles, m customers, one route per vehicle, and each customer is served a single time.

The Capacitated VRP (CVRP) is a VRP variant, which designs optimal delivery routes where each vehicle only travels one route, each vehicle has the same characteristics and there is only one  central  depot.  The  goal  of  the  VRP  is  to  find  a set  of  least-cost  vehicle  routes  such  that each customer is visited exactly once by one vehicle, each vehicle starts and ends its route at the depot, and the capacity of the vehicles is not exceeded.

Our goal in this 4 months UTBM project is to develop an approach on how to solve CVRP problems.

Made by :

<a href=https://github.com/KwassiSenam>Sonia Kwassi</a>,
<a href=https://github.com/Axelvel>Axel Velez</a>,
<a href=https://github.com/galyfray>Cyril Obrecht</a>,
<a href=https://github.com/m-aspro>Marie Aspro</a>,
<a href=https://github.com/nexowo>Jean Maccou</a>

# Developement environment. 

In order to setup the developpement environment you will first need to install anaconda (conda not miniconda. Installing through pip won't work) and make. For windows user make sure that the make executable is in your path.

Windows user will be needed to use the conda powershell prompt for the following command to work.

Then run `make init` to initialize the virtual environment and `make run` to start the program. Refer to `make help` for a complete and up to date list of the commands.