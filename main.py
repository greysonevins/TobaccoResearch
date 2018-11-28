from PLOSApiSearch import TobaccoPLOSData
from DOAJApiSearch import DOAJDateVerify
from finalResults import FinalizeResults


def main():
    print("=== Process 1 Start ==== ")
    print(" == API From Plos ==")
    print()
    TobaccoPlos = TobaccoPLOSData()
    TobaccoPlos.plos_job()

    print("\n\n")
    print("=== Process 2 Start ==== ")
    print(" == Verify From DOAJ ==")
    print("\n\n")

    DOAJVerify = DOAJDateVerify()
    DOAJVerify.doaj_verify()

    print("\n\n")
    print("=== Process 3 Start ==== ")
    print(" == Final Results ==")
    print("\n\n")

    FinalizeResults().getResults()

    print("\n\n")
    print("=====Completed All Processes======")

if __name__ == "__main__":
    main()
