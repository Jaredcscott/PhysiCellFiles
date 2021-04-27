/*
###############################################################################
# If you use PhysiCell in your project, please cite PhysiCell and the version #
# number, such as below:                                                      #
#                                                                             #
# We implemented and solved the model using PhysiCell (Version x.y.z) [1].    #
#                                                                             #
# [1] A Ghaffarizadeh, R Heiland, SH Friedman, SM Mumenthaler, and P Macklin, #
#     PhysiCell: an Open Source Physics-Based Cell Simulator for Multicellu-  #
#     lar Systems, PLoS Comput. Biol. 14(2): e1005991, 2018                   #
#     DOI: 10.1371/journal.pcbi.1005991                                       #
#                                                                             #
# See VERSION.txt or call get_PhysiCell_version() to get the current version  #
#     x.y.z. Call display_citations() to get detailed information on all cite-#
#     able software used in your PhysiCell application.                       #
#                                                                             #
# Because PhysiCell extensively uses BioFVM, we suggest you also cite BioFVM  #
#     as below:                                                               #
#                                                                             #
# We implemented and solved the model using PhysiCell (Version x.y.z) [1],    #
# with BioFVM [2] to solve the transport equations.                           #
#                                                                             #
# [1] A Ghaffarizadeh, R Heiland, SH Friedman, SM Mumenthaler, and P Macklin, #
#     PhysiCell: an Open Source Physics-Based Cell Simulator for Multicellu-  #
#     lar Systems, PLoS Comput. Biol. 14(2): e1005991, 2018                   #
#     DOI: 10.1371/journal.pcbi.1005991                                       #
#                                                                             #
# [2] A Ghaffarizadeh, SH Friedman, and P Macklin, BioFVM: an efficient para- #
#     llelized diffusive transport solver for 3-D biological simulations,     #
#     Bioinformatics 32(8): 1256-8, 2016. DOI: 10.1093/bioinformatics/btv730  #
#                                                                             #
###############################################################################
#                                                                             #
# BSD 3-Clause License (see https://opensource.org/licenses/BSD-3-Clause)     #
#                                                                             #
# Copyright (c) 2015-2018, Paul Macklin and the PhysiCell Project             #
# All rights reserved.                                                        #
#                                                                             #
# Redistribution and use in source and binary forms, with or without          #
# modification, are permitted provided that the following conditions are met: #
#                                                                             #
# 1. Redistributions of source code must retain the above copyright notice,   #
# this list of conditions and the following disclaimer.                       #
#                                                                             #
# 2. Redistributions in binary form must reproduce the above copyright        #
# notice, this list of conditions and the following disclaimer in the         #
# documentation and/or other materials provided with the distribution.        #
#                                                                             #
# 3. Neither the name of the copyright holder nor the names of its            #
# contributors may be used to endorse or promote products derived from this   #
# software without specific prior written permission.                         #
#                                                                             #
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" #
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE   #
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE  #
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE   #
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR         #
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF        #
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS    #
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN     #
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)     #
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE  #
# POSSIBILITY OF SUCH DAMAGE.                                                 #
#                                                                             #
###############################################################################
*/

#include "./culturedMeat.h"
#include "../modules/PhysiCell_settings.h"

void create_cell_types( void )
{
	// set the random seed 
	SeedRandom( parameters.ints("random_seed") );  
	
	/* 
	   Put any modifications to default cell definition here if you 
	   want to have "inherited" by other cell types. 
	   
	   This is a good place to set default functions. 
	*/ 
	
	initialize_default_cell_definition(); 

	cell_defaults.parameters.o2_proliferation_saturation = 38.0;  
	cell_defaults.parameters.o2_reference = 38.0; 
	
	cell_defaults.functions.update_phenotype = tumor_cell_phenotype_with_oncoprotein;  
	cell_defaults.functions.volume_update_function = standard_volume_update_function;
	cell_defaults.functions.update_velocity = standard_update_cell_velocity;	
	
 	/*
	   This parses the cell definitions in the XML config file. 
	*/
	
	initialize_cell_definitions_from_pugixml(); 
	
	/* 
	   Put any modifications to individual cell definitions here. 
	   
	   This is a good place to set custom functions. 
	*/ 
	
	/*
	   This builds the map of cell definitions and summarizes the setup. 
	*/
		
	build_cell_definitions_maps(); 
	display_cell_definitions( std::cout ); 
	
	return; 
}

void setup_microenvironment( void )
{// make sure ot override and go back to 2D 
	if( default_microenvironment_options.simulate_2D == false )
	{
		std::cout << "Warning: overriding XML config option and setting to 2D!" << std::endl; 
		default_microenvironment_options.simulate_2D = true; 
	}
	// set domain parameters
	initialize_microenvironment(); 
	//Adding in director signal env parameters
	int director_index = microenvironment.find_density_index( "director signal" ); 
	microenvironment.diffusion_coefficients[director_index] = 
		parameters.doubles("director_signal_D");  
	microenvironment.decay_rates[director_index] = 
		parameters.doubles("director_signal_decay"); 
	return; 
}	

void setup_tissue( void )
{
	//Chooses the number of directors to place. 
	int number_of_directors = parameters.ints("number_of_directors"); 
	double cell_radius = cell_defaults.phenotype.geometry.radius; 
	double cell_spacing = 0.95 * 2.0 * cell_radius; 
	
	double tumor_radius = parameters.doubles( "tumor_radius" );
	
	// Parameter<double> temp; 
	
	int i = parameters.doubles.find_index( "tumor_radius" ); 
	
	Cell* pCell = NULL; 

	
	double x = 0.0; 
	double x_outer = tumor_radius; 
	double y = 0.0; 
	
	double p_mean = parameters.doubles( "oncoprotein_mean" ); 
	double p_sd = parameters.doubles( "oncoprotein_sd" ); 
	double p_min = parameters.doubles( "oncoprotein_min" ); 
	double p_max = parameters.doubles( "oncoprotein_max" ); 
	std::vector<double> position(3,0.0);
	double x_range = default_microenvironment_options.X_range[1] - default_microenvironment_options.X_range[0]; 
	double y_range = default_microenvironment_options.Y_range[1] - default_microenvironment_options.Y_range[0]; 

	double relative_margin = 0.2;  
	double relative_outer_margin = 0.02;  

	//Start of csv reader
	std::string filename = "./coords.csv";
	std::ifstream file( filename, std::ios::in );
	if( !file )
	{ 
		//Checking if the file exists
		std::cout << "Error: " << filename << " not found during cell loading. Quitting." << std::endl; 
		exit(-1);
	}
	std::string line;
	while (std::getline(file, line))
	{
		//Reading lines 
		std::vector<double> data;
		csv_to_vector( line.c_str() , data ); 

		if( data.size() != 4 )
		{
			//Type ID is specified in the .xml file under cell definitions
			std::cout << "Error! Importing cells from a CSV file expects each row to be x,y,z,typeID." << std::endl;  
			exit(-1);
		}

		std::vector<double> position = { data[0] , data[1] , data[2] }; //Creating position array with x,y,z, coords from csv

		int my_type = (int) data[3]; 
		Cell_Definition* pCD = find_cell_definition( my_type ); //Assigning type to cell 
		if( pCD != NULL )
		{
			std::cout << "Creating " << pCD->name << " (type=" << pCD->type << ") at " 
			<< position << std::endl; 
			Cell* pCell = create_cell( *pCD ); 
			pCell->assign_position( position ); //Assigning position to cell
		}
		else
		{
			std::cout << "Warning! No cell definition found for index " << my_type << "!" << std::endl
			<< "\tIgnoring cell in " << filename << " at position " << position << std::endl; 
		}

	}
	file.close();  //Closing file 
	//End of csv reader  
	int n = 0;
	for( int i=0; i < number_of_directors ; i++ )
	{
		// pick a random location 
		position[0] = default_microenvironment_options.X_range[0] + x_range*( relative_margin + (1.0-2*relative_margin)*UniformRandom() ); 
		
		position[1] = default_microenvironment_options.Y_range[0] + y_range*( relative_outer_margin + (1.0-2*relative_outer_margin)*UniformRandom() ); 
		
		// place the cell
		Cell* pC;
		pC = create_cell( director_cell ); 
		pC->assign_position( position );
		pC->is_movable = false; 
	} 
	while( y < tumor_radius )
	{
		x = 0.0; 
		if( n % 2 == 1 )
		{ x = 0.5*cell_spacing; }
		x_outer = sqrt( tumor_radius*tumor_radius - y*y ); 
		
		while( x < x_outer )
		{
			pCell = create_cell(); // tumor cell 
			pCell->assign_position( x , y , 0.0 );
			pCell->custom_data[0] = NormalRandom( p_mean, p_sd );
			if( pCell->custom_data[0] < p_min )
			{ pCell->custom_data[0] = p_min; }
			if( pCell->custom_data[0] > p_max )
			{ pCell->custom_data[0] = p_max; }
			
			if( fabs( y ) > 0.01 )
			{
				pCell = create_cell(); // tumor cell 
				pCell->assign_position( x , -y , 0.0 );
				pCell->custom_data[0] = NormalRandom( p_mean, p_sd );
				if( pCell->custom_data[0] < p_min )
				{ pCell->custom_data[0] = p_min; }
				if( pCell->custom_data[0] > p_max )
				{ pCell->custom_data[0] = p_max; }				
			}
			
			if( fabs( x ) > 0.01 )
			{ 
				pCell = create_cell(); // tumor cell 
				pCell->assign_position( -x , y , 0.0 );
				pCell->custom_data[0] = NormalRandom( p_mean, p_sd );
				if( pCell->custom_data[0] < p_min )
				{ pCell->custom_data[0] = p_min; }
				if( pCell->custom_data[0] > p_max )
				{ pCell->custom_data[0] = p_max; }
		
				if( fabs( y ) > 0.01 )
				{
					pCell = create_cell(); // tumor cell 
					pCell->assign_position( -x , -y , 0.0 );
					pCell->custom_data[0] = NormalRandom( p_mean, p_sd );
					if( pCell->custom_data[0] < p_min )
					{ pCell->custom_data[0] = p_min; }
					if( pCell->custom_data[0] > p_max )
					{ pCell->custom_data[0] = p_max; }
				}
			}
			x += cell_spacing; 
			
		}
		
		y += cell_spacing * sqrt(3.0)/2.0; 
		n++; 
	}
	
	double sum = 0.0; 
	double min = 9e9; 
	double max = -9e9; 
	for( int i=0; i < all_cells->size() ; i++ )
	{
		double r = (*all_cells)[i]->custom_data[0]; 
		sum += r;
		if( r < min )
		{ min = r; } 
		if( r > max )
		{ max = r; }
	}
	double mean = sum / ( all_cells->size() + 1e-15 ); 
	// compute standard deviation 
	sum = 0.0; 
	for( int i=0; i < all_cells->size(); i++ )
	{
		sum +=  ( (*all_cells)[i]->custom_data[0] - mean )*( (*all_cells)[i]->custom_data[0] - mean ); 
	}
	double standard_deviation = sqrt( sum / ( all_cells->size() - 1.0 + 1e-15 ) ); 
	
	std::cout << std::endl << "Oncoprotein summary: " << std::endl
			  << "===================" << std::endl; 
	std::cout << "mean: " << mean << std::endl; 
	std::cout << "standard deviation: " << standard_deviation << std::endl; 
	std::cout << "[min max]: [" << min << " " << max << "]" << std::endl << std::endl; 
	
	return; 
}

//Adding in director cell rule
void director_cell_rule( Cell* pCell , Phenotype& phenotype , double dt )
{
	return; 
	std::vector<Cell*> nearby = pCell->cells_in_my_container(); 
	
	// if at least 2 neighbors, turn off secretion 
		// if size >= 3, then we have "self" and at least two more 
	if( nearby.size() > 2 )
	{
		pCell->phenotype.secretion.set_all_secretion_to_zero(); 
		pCell->custom_data[ "secreting" ] = 0.0; 
		
		pCell->functions.update_phenotype = NULL; 
	}
	
	return; 
}

// custom cell phenotype function to scale immunostimulatory factor with hypoxia 
void tumor_cell_phenotype_with_oncoprotein( Cell* pCell, Phenotype& phenotype, double dt )
{
	update_cell_and_death_parameters_O2_based(pCell,phenotype,dt);
	
	// if cell is dead, don't bother with future phenotype changes. 
	if( phenotype.death.dead == true )
	{
		pCell->functions.update_phenotype = NULL; 		
		return; 
	}

	// multiply proliferation rate by the oncoprotein 
	
	static int cycle_start_index = live.find_phase_index( PhysiCell_constants::live ); 
	static int cycle_end_index = live.find_phase_index( PhysiCell_constants::live ); 
	static int oncoprotein_i = pCell->custom_data.find_variable_index( "oncoprotein" ); 

	phenotype.cycle.data.transition_rate( cycle_start_index ,cycle_end_index ) *= pCell->custom_data[oncoprotein_i] ; 
	
	return; 
}

std::vector<std::string> heterogeneity_coloring_function( Cell* pCell )
{
	static int oncoprotein_i = pCell->custom_data.find_variable_index( "oncoprotein" ); 
	static std::string director_color = parameters.strings( "director_color" ); 
	
	static double p_min = parameters.doubles( "oncoprotein_min" ); 
	static double p_max = parameters.doubles( "oncoprotein_max" ); 
	
	// immune are black
	std::string color = "black";
	std::vector< std::string > output( 4, "black" ); 
	if( pCell->type == director_ID )
	{ color = director_color; 
		output[0] = color; 
		output[2] = color; 
	
		return output;
	}

	if( pCell->type == 1 )
	{ return output; } 
	
	// live cells are green, but shaded by oncoprotein value 
	if( pCell->phenotype.death.dead == false )
	{
		int oncoprotein = (int) round( (1.0/(p_max-p_min)) * (pCell->custom_data[oncoprotein_i]-p_min) * 255.0 ); 
		char szTempString [128];
		sprintf( szTempString , "rgb(%u,%u,%u)", oncoprotein, oncoprotein, 255-oncoprotein );
		output[0].assign( szTempString );
		output[1].assign( szTempString );

		sprintf( szTempString , "rgb(%u,%u,%u)", (int)round(output[0][0]/p_max) , (int)round(output[0][1]/p_max) , (int)round(output[0][2]/p_max) );
		output[2].assign( szTempString );
		
		return output; 
	}

	// if not, dead colors 
	
	if (pCell->phenotype.cycle.current_phase().code == PhysiCell_constants::apoptotic )  // Apoptotic - Red
	{
		output[0] = "rgb(255,0,0)";
		output[2] = "rgb(125,0,0)";
	}
	
	// Necrotic - Brown
	if( pCell->phenotype.cycle.current_phase().code == PhysiCell_constants::necrotic_swelling || 
		pCell->phenotype.cycle.current_phase().code == PhysiCell_constants::necrotic_lysed || 
		pCell->phenotype.cycle.current_phase().code == PhysiCell_constants::necrotic )
	{
		output[0] = "rgb(250,138,38)";
		output[2] = "rgb(139,69,19)";
	}	
	
	return output; 
}