import azure.functions as func

import src.utils.functions as f

def main(
    timer: func.TimerRequest,
):
    # if this operation works, then msi client id works
    secrets = f.get_secrets_dict()

if __name__ == "__main__":
    main()
