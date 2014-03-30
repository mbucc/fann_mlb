#include "fann.h"

int main()
{
    const unsigned int layers_n = 4;
    const unsigned int nodes_per_layer[] = {93, 60, 20, 1};

    const float desired_error = (const float) 0.0000005;
    const unsigned int max_epochs = 10000;
    const unsigned int epochs_between_reports = 1000;

    struct fann *ann = fann_create_standard_array(layers_n, nodes_per_layer);

    fann_set_activation_function_hidden(ann, FANN_SIGMOID_SYMMETRIC);
    fann_set_activation_function_output(ann, FANN_SIGMOID_SYMMETRIC);

    fann_train_on_file(ann, "firstplace.dat", max_epochs,
        epochs_between_reports, desired_error);

    fann_save(ann, "firstplace.net");

    fann_destroy(ann);

    return 0;
}
