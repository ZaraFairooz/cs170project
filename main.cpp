#include <iostream>
#include <sstream>
#include <fstream>
#include <vector>
#include <queue>
#include <algorithm>
#include <iterator>


using namespace std;


struct FeatureSet {
   double accuracy;
   vector<int> selected_features;


   bool operator<(const FeatureSet& other) const {
       return accuracy < other.accuracy;
   }


   vector<int> incrementIndices(const vector<int>& features) const {
       vector<int> incremented_features = features;
       for (int& feature : incremented_features) {
           feature += 1;
       }
       return incremented_features;
   }


   void display() const {
       vector<int> incremented_features = incrementIndices(selected_features);
       ostringstream oss;


       if (!incremented_features.empty()) {
           copy(incremented_features.begin(), incremented_features.end() - 1,
                ostream_iterator<int>(oss, ","));
           oss << incremented_features.back();
       }


       cout << "Feature set {" << oss.str() << "} with accuracy: " << accuracy << endl;
   }
};


vector<Instance> parseInputFile(const string& filename) {
   ifstream file_stream(filename);
   vector<Instance> instances;


   while (file_stream.good()) {
       Instance instance;
       double label = INT_MAX;
       vector<double> feature_values;
       double value;


       string line;
       getline(file_stream, line);


       istringstream line_stream(line);
       line_stream >> label;


       if (label == INT_MAX) {
           break;
       }


       instance.set_type(label);


       while (line_stream >> value) {
           instance.append_feature(value);
       }


       instances.push_back(instance);
   }


   return instances;
}


bool isFeatureSelected(int feature, const vector<int>& feature_set) {
   return find(feature_set.begin(), feature_set.end(), feature) != feature_set.end();
}


void evaluation() {
   percentage = static_cast<double>(rand()) / RAND_MAX * 1000.0;
   percentage = round(percentage * 10.0) / 10.0;
}


static double getEvaluation () {
   return percentage;
}


void performForwardSelection(Problem& problem, int num_features) {
   cout << "This dataset has " << num_features << " features with "
        << problem.dataset_size() << " instances:" << endl << endl;


   priority_queue<FeatureSet> feature_queue;
   FeatureSet best_feature_set;
   best_feature_set.accuracy = 0;


   FeatureSet current_feature_set;
   current_feature_set.selected_features = {};
   current_feature_set.accuracy = problem.Nearest_N(current_feature_set.selected_features);
   current_feature_set.display();


   vector<int> selected_features;
   bool accuracy_warning = true;


   for (int round = 0; round < num_features; ++round) {
       for (int feature = 0; feature < num_features; ++feature) {
           if (isFeatureSelected(feature, selected_features)) {
               continue;
           }


           FeatureSet candidate_feature_set;
           candidate_feature_set.selected_features = selected_features;
           candidate_feature_set.selected_features.push_back(feature);
           candidate_feature_set.accuracy = problem.Nearest_N(candidate_feature_set.selected_features);
           feature_queue.push(candidate_feature_set);
       }


       current_feature_set = feature_queue.top();
       if (current_feature_set.accuracy > best_feature_set.accuracy) {
           best_feature_set = current_feature_set;
       }


       if (accuracy_warning && current_feature_set.accuracy < best_feature_set.accuracy) {
           accuracy_warning = false;
           cout << endl << "Warning: accuracy decreasing, continuing search..." << endl << endl;
       }


       current_feature_set.display();
       selected_features = current_feature_set.selected_features;


       while (!feature_queue.empty()) {
           feature_queue.pop();
       }
   }


   cout << endl << "The best feature subset is: ";
   best_feature_set.display();
}


void performBackwardElimination(Problem& problem, int num_features) {
   cout << "This dataset has " << num_features << " features with "
        << problem.dataset_size() << " instances:" << endl << endl;


   priority_queue<FeatureSet> feature_queue;
   FeatureSet best_feature_set;
   best_feature_set.accuracy = 0;


   FeatureSet current_feature_set;
   vector<int> selected_features(num_features);
   iota(selected_features.begin(), selected_features.end(), 0);


   current_feature_set.selected_features = selected_features;
   current_feature_set.accuracy = problem.Nearest_N(current_feature_set.selected_features);
   current_feature_set.display();


   bool accuracy_warning = true;


   for (int round = 0; round < num_features; ++round) {
       for (int feature = 0; feature < num_features; ++feature) {
           if (!isFeatureSelected(feature, selected_features)) {
               continue;
           }


           FeatureSet candidate_feature_set;
           candidate_feature_set.selected_features = selected_features;
           candidate_feature_set.selected_features.erase(
               remove(candidate_feature_set.selected_features.begin(),
                      candidate_feature_set.selected_features.end(),
                      feature),
               candidate_feature_set.selected_features.end());
           candidate_feature_set.accuracy = problem.Nearest_N(candidate_feature_set.selected_features);
           feature_queue.push(candidate_feature_set);
       }


       current_feature_set = feature_queue.top();
       if (current_feature_set.accuracy > best_feature_set.accuracy) {
           best_feature_set = current_feature_set;
       }


       if (accuracy_warning && current_feature_set.accuracy < best_feature_set.accuracy) {
           accuracy_warning = false;
           cout << endl << "Warning: accuracy decreasing, continuing search..." << endl << endl;
       }


       current_feature_set.display();
       selected_features = current_feature_set.selected_features;


       while (!feature_queue.empty()) {
           feature_queue.pop();
       }
   }


   cout << endl << "The best feature subset is: ";
   best_feature_set.display();
}


int main(int argc, char* argv[]) {
   if (argc != 2) {
       cout << "Error: Invalid program call" << endl;
       return 1;
   }


   string input_file(argv[1]);
   vector<Instance> instances = parseInputFile(input_file);


   Problem problem(instances);
   int num_features = instances.at(0).get_features().size();


   cout << "Welcome to the Feature Selection Algorithm" << endl;
   cout << "Choose the selection algorithm:" << endl;
   cout << "\t1) Forward Selection" << endl;
   cout << "\t2) Backward Elimination" << endl;


   int choice;
   cin >> choice;


   if (choice == 1) {
       performForwardSelection(problem, num_features);
   } else {
       performBackwardElimination(problem, num_features);
   }


   return 0;
}
