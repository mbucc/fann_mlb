#include "fann.h"

int main()
{
    const unsigned int num_input = 93;
    const unsigned int num_output = 1;
    const unsigned int num_layers = 4;
    const unsigned int num_neurons_hidden_layer1 = 60;
    const unsigned int num_neurons_hidden_layer2 = 20;
    const float desired_error = (const float) 0.0000005;
    const unsigned int max_epochs = 10000;
    const unsigned int epochs_between_reports = 1000;

    struct fann *ann = 0;
    if (num_layers == 3)
	    ann = fann_create_standard(
			    3
			    , num_input
			    , num_neurons_hidden_layer1
			    , num_output
			    );
    else if (num_layers == 4)
	    ann = fann_create_standard(
			    4
			    , num_input
			    , num_neurons_hidden_layer1
			    , num_neurons_hidden_layer2
			    , num_output
			    );
    else {
	    fputs("Invalid number of layers.", stderr);
	    exit(1);
    }

    fann_set_activation_function_hidden(ann, FANN_SIGMOID_SYMMETRIC);
    fann_set_activation_function_output(ann, FANN_SIGMOID_SYMMETRIC);

    fann_train_on_file(ann, "firstplace.dat", max_epochs,
        epochs_between_reports, desired_error);

    fann_save(ann, "firstplace.net");

    fann_destroy(ann);

    return 0;
}
