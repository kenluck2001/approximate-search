from Person import PersonIterator

if __name__ == "__main__":
    filename = "data/simple_test_file.csv"
    personIter = PersonIterator(filename)

    # find all the relatives of Xavier William-Scott
    personIter.printRelatives("Xavier", "William-Scott")
    # find all the relatives of Jane xxxx
    personIter.printRelatives("jane", "xxxx")


