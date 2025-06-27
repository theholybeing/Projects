#include <iostream>
#include <fstream>
#include <string>
#include <cstdlib> //? for exit() function
using namespace std;

string name, address, gender, bloodGroup, diseaseName, cnic;
int patientId = 0;
int age;
long long int contact;
void exit_from_program(); //?Prototype of Exit function

void getpatientdetails()
{
    cout << "Enter Name: ";
    while (cin.get() != '\n')
        ;
    getline(cin, name);
    cout << "Enter Your Address: ";
    getline(cin, address);
    cout << "Enter Your CNIC: "; //?Getting Details from Patient
    getline(cin, cnic);
    cout << "Enter Your Contact Number: ";
    cin >> contact;
    cout << "Enter Your Gender: ";
    while (cin.get() != '\n')
        ;
    getline(cin, gender);
    cout << "Enter Your Age: ";
    cin >> age;
    cout << "Enter Your BloodGroup: ";
    while (cin.get() != '\n')
        ;
    getline(cin, bloodGroup);
    cout << "Enter Your DiseaseName: ";
    getline(cin, diseaseName);
    cout << endl;
    if (diseaseName == "eye" || diseaseName == "Eye") //? Allocating Patient
    {
        cout << "Go to room no. 10\nEye Speacialist Dr. Hasnain Mustafa";
    }
    else if (diseaseName == "heart" || diseaseName == "Heart")
    {
        cout << "Go to room no. 10\nHeart Seorgen Dr. Aqeel Ahmad";
    }
    else if (diseaseName == "diabetes" || diseaseName == "Diabetes")
    {
        cout << "Go to room no. 10\nDiabetes and Insuline Speacialist Dr. Haider Ali";
    }
    else if (diseaseName == "hypertension" || diseaseName == "Hypertension")
    {
        cout << "Go to room no. 10\nBP Speacialist Dr. Alizay Shah";
    }
    else if (diseaseName == "kidney" || diseaseName == "Kidney")
    {
        cout << "Go to room no. 10\nKidney Speacialist Dr. Nouman Ahmad";
    }
    else if (diseaseName == "Liver" || diseaseName == "liver")
    {
        cout << "Go to room no. 10\nLiver Speacialist Dr. Muhammad Ali";
    }
    else if (diseaseName == "lungs" || diseaseName == "Lungs")
    {
        cout << "Go to room no. 10\nLungs Speacialist Dr. Ghulam Mustafa";
    }
    else if (diseaseName == "no" || diseaseName == "No")
    {
        cout << "OK! Your record has been saved.";
    }
    else
    {
        cout << "Go to room no. 10\nMBBS Dr. Muneer Saqiq";
    }
    cout << "\n\n\n\t\t    -|-|-|-|-|-|-|-|-|-|-|-|-|-|--&(-^-)&--|-|-|-|-|-|-|-|-|-|-|-|-|-|-\n\n\n";
    int menue;
    cout << "\nENTER \"0\" FOR EXIT THE PROGRAM AND \"1\" FOR MAIN MENU\n";
    cin >> menue; //? Asking for Main Menu
    switch (menue)
    {
    case 0:
        exit_from_program();
        break;
    case 1:

        break;
    }

    patientId++;
}

void savePatientinfo()
{ //? Saving Details in File
    ofstream savepatientfiling;
    savepatientfiling.open("Patient Details.txt", ios::app);
    savepatientfiling << "Patient's CNIC " << cnic << "." << endl;
    savepatientfiling << "Patient ID " << patientId << "." << endl;
    savepatientfiling << "Patient Name " << name << "." << endl;
    savepatientfiling << "Patient's Address " << address << "." << endl;
    savepatientfiling << "Patient's CNIC " << cnic << "." << endl;
    savepatientfiling << "Patient's Contact Number " << contact << "." << endl;
    savepatientfiling << "Patient's Age " << age << "." << endl;
    savepatientfiling << "Patient's Gender " << gender << "." << endl;
    savepatientfiling << "Patient's BloodGroup " << bloodGroup << "." << endl;
    savepatientfiling << "Patient's Disease " << diseaseName << ".\n\n"
                      << endl;
    savepatientfiling.close();
}

void displaydetails()
{ //? Displaying Patient Details
    string cnic_no;
    cout << "Enter your CNIC number:";
    while (cin.get() != '\n')
        ;
    getline(cin, cnic_no);
    ifstream read_details;
    read_details.open("Patient Details.txt");

    string cnic_into_string = "Patient's CNIC " + cnic_no + ".";
    bool found = false;

    if (read_details.is_open())
    {
        string matching;
        while (!read_details.eof())
        {
            getline(read_details, matching);

            if (matching == cnic_into_string)
            {
                cout << "Details of the Patient are following:\n\n";
                string extract_details;
                found = true;

                for (int i = 1; i <= 9; i++)
                {
                    getline(read_details, extract_details);
                    cout << extract_details << endl;
                }
            }
        }
        if (!found)
        {
            cout << "Sorry! this patient is not exist here!!" << endl;
        }
    }
    else
    {
        cout << "\nFile Openning error!";
    }
    read_details.close();
    cout << "\n\n\n\t\t    -|-|-|-|-|-|-|-|-|-|-|-|-|-|--&(-^-)&--|-|-|-|-|-|-|-|-|-|-|-|-|-|-\n\n\n";
    int menue;
    cout << "\nENTER \"0\" FOR EXIT THE PROGRAM AND \"1\" FOR MAIN MENU\n";
    cin >> menue;
    //? Asking for Menu
    switch (menue)
    {
    case 0:
        exit_from_program();
        break;
    case 1:

        break;
    }
}

void deletePatientRecord()
{ //? Deleting Specific Patient Details from File
    string cnic_no;
    cout << "Enter CNIC number to delete the record: ";
    while (cin.get() != '\n')
        ;
    getline(cin, cnic_no);

    ifstream inputFile("Patient Details.txt");
    ofstream tempFile("temp.txt");

    if (inputFile.is_open() && tempFile.is_open())
    {
        string line;
        bool found = false;

        while (getline(inputFile, line))
        {
            if ("Patient's CNIC " + cnic_no + "." == line)
            {
                found = true;
                //? Skip this record, don't write it to the temporary file
                for (int i = 0; i < 9; i++)
                {
                    getline(inputFile, line);
                }
            }
            else
            {

                tempFile << line << endl;
            }
        }

        inputFile.close();
        tempFile.close();

        if (found)
        {
            remove("Patient Details.txt");             //? Remove the old file
            rename("temp.txt", "Patient Details.txt"); //? Rename the temporary file
            cout << "Record with CNIC " << cnic_no << " deleted successfully." << endl;
        }
        else
        {
            cout << "Record with CNIC " << cnic_no << " not found." << endl;
            remove("temp.txt"); //? Delete the temporary file if no record was found
        }
    }
    else
    {
        cout << "Error opening files." << endl;
    }
    cout << "\n\n\n\t\t    -|-|-|-|-|-|-|-|-|-|-|-|-|-|--&(-^-)&--|-|-|-|-|-|-|-|-|-|-|-|-|-|-\n\n\n";
    int menue;
    cout << "\nENTER \"0\" FOR EXIT THE PROGRAM AND \"1\" FOR MAIN MENU\n";
    cin >> menue;
    switch (menue)
    { //? Asking for Main Menu
    case 0:
        exit_from_program();
        break;
    case 1:

        break;
    }
}
void updatePatientRecord()
{
    string new_cnic_no;
    cout << "Enter CNIC number to update the record: ";
    while (cin.get() != '\n')
        ;
    getline(cin, new_cnic_no);
    ifstream inputFile("Patient Details.txt");
    ofstream tempFile("temp.txt");

    if (inputFile.is_open() && tempFile.is_open())
    {
        string line;
        bool found = false;

        while (getline(inputFile, line))
        {
            if ("Patient's CNIC " + new_cnic_no + "." == line)
            {
                found = true;
                //? Skip this record, don't write it to the temporary file
                for (int i = 0; i < 9; i++)
                {
                    getline(inputFile, line);
                }
                //?Taking new record
                cout << "Enter New data :\n";
                cout << "Enter Name: ";
                getline(cin, name);
                cout << "Enter Your Address: ";
                getline(cin, address);
                cout << "Enter Your CNIC: ";
                getline(cin, cnic);
                cout << "Enter Your Contact Number: ";
                cin >> contact;
                cout << "Enter Your Gender ";
                while (cin.get() != '\n')
                    ;
                getline(cin, gender);
                cout << "Enter Your Age: ";
                cin >> age;
                cout << "Enter Your BloodGroup: ";
                while (cin.get() != '\n')
                    ;
                getline(cin, bloodGroup);
                cout << "Enter Your DiseaseName: ";
                getline(cin, diseaseName);
                tempFile << "Patient's CNIC " << cnic << "." << endl;
                tempFile << "Patient ID " << patientId << "." << endl;
                //?Writing new data in temporary  file
                tempFile << "Patient Name " << name << "." << endl;
                tempFile << "Patient's Address " << address << "." << endl;
                tempFile << "Patient's CNIC " << cnic << "." << endl;
                tempFile << "Patient's Contact Number " << contact << "." << endl;
                tempFile << "Patient's Age " << age << "." << endl;
                tempFile << "Patient's Gender " << gender << "." << endl;
                tempFile << "Patient's BloodGroup " << bloodGroup << "." << endl;
                tempFile << "Patient's Disease " << diseaseName << ".\n\n"
                         << endl;
            }
        }

        inputFile.close();
        tempFile.close();

        if (found)
        {
            remove("Patient Details.txt");             //? Remove the old file
            rename("temp.txt", "Patient Details.txt"); //? Rename the temporary file
            cout << "Record  updated successfully." << endl;
        }
        else
        {
            cout << "Record with CNIC " << new_cnic_no << " not found." << endl;
            remove("temp.txt"); //? Delete the temporary file if no record was found
        }
    }
    else
    {
        cout << "Error opening files." << endl;
    }
    cout << "\n\n\n\t\t    -|-|-|-|-|-|-|-|-|-|-|-|-|-|--&(-^-)&--|-|-|-|-|-|-|-|-|-|-|-|-|-|-\n\n\n";
    int menue;
    cout << "\nENTER \"0\" FOR EXIT THE PROGRAM AND \"1\" FOR MAIN MENU\n";
    cin >> menue;
    switch (menue)
    { //? Asking for Main Menu
    case 0:
        exit_from_program();
        break;
    case 1:

        break;
    }
}
void exit_from_program()
{
    cout << "\nTHANKs For Using Program\nNow Program has been exit." << endl;
    exit(0);
}

int main()
{
    int choice;
    while (true)
    {
        system("CLS");
        cout << "==================================================================================================================" << endl;
        cout << "==================================================================================================================\n"
             << endl;
        cout << "\t\t           H   H    OOO    SSSSS   PPPP  IIII  TTTTTTT    A      LL    " << endl;
        cout << "\t\t           H   H   O   O   S       P  P   II     TT      A A     LL    " << endl;
        cout << "\t\t           HHHHH   O   O   SSSSS   PPP    II     TT     AAAAA    LL    " << endl;
        cout << "\t\t           H   H   O   O       S   P      II     TT    A     A   LL    " << endl;
        cout << "\t\t           H   H    OOO    SSSSS   P     IIII    TT   A       A  LLLLLLLL " << endl;
        cout << "\n==================================================================================================================" << endl;
        cout << "==================================================================================================================\n\n"
             << endl;
        cout << "1. Add New Patient Record.\n";
        cout << "2. View Patient History.\n";
        cout << "3. Delete Patient Record.\n";
        cout << "4. Update Patient Record.\n";
        cout << "5. Exit\n";
        cout << "Choose an Option: ";
        cin >> choice;
        system("CLS");

        switch (choice)
        {
        case 1:
            getpatientdetails();
            savePatientinfo();
            break;
        case 2:
            displaydetails();
            break;
        case 3:
            deletePatientRecord();
            break;
        case 4:
            updatePatientRecord();
            break;
        case 5:
            exit_from_program();
            break;
        default:
            cout << "You chose an invalid option.\n";
        }

        cout << "\n\n\t\t    -|-|-|-|-|-|-|-|-|-|-|-|-|-|--&(-^-)&--|-|-|-|-|-|-|-|-|-|-|-|-|-|-\n\n\n";
    }

    return 0;
}
