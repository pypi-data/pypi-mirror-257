import os
from izio_cli.helper.console_helper import run_command


def setupFirebase(flavor, root):
    # get android firebase json
    run_command(
        [
            "cp",
            f"{root}/firebase/android/google-services-{flavor}.json",
            f"{root}/loyalty2_0/android/app/src/prod/google-services.json",
        ],
        path=root,
        silent=True,
    )
    # get ios firebase json
    run_command(
        [
            "cp",
            f"{root}/firebase/apple/GoogleService-Info-{flavor}.plist",
            f"{root}/loyalty2_0/ios/Runner/prod/GoogleService-Info.plist",
        ],
        path=root,
        silent=True,
    )


def changeOnesignalIcons(root):
    base_path = f"{root}/loyalty2_0/android/app/src/prod/res"
    # create drwable folders
    folders = [
        "drawable-mdpi",
        "drawable-hdpi",
        "drawable-xhdpi",
        "drawable-xxhdpi",
        "drawable-xxxhdpi",
    ]
    for folder in folders:
        os.makedirs(f"{base_path}/{folder}", exist_ok=True)

    files = {
        "mipmap-hdpi/ic_launcher.png": "drawable-mdpi/ic_stat_onesignal_default.png",
        "mipmap-mdpi/ic_launcher.png": "drawable-hdpi/ic_stat_onesignal_default.png",
        "mipmap-xhdpi/ic_launcher.png": "drawable-xhdpi/ic_stat_onesignal_default.png",
        "mipmap-xxhdpi/ic_launcher.png": "drawable-xxhdpi/ic_stat_onesignal_default.png",
        "mipmap-xxxhdpi/ic_launcher.png": "drawable-xxxhdpi/ic_stat_onesignal_default.png",
        "mipmap-xxxhdpi/ic_launcher.png": "drawable-xxxhdpi/ic_onesignal_large_icon_default.png",
    }
    for file, new_file in files.items():
        run_command(
            ["cp", f"{base_path}/{file}", f"{base_path}/{new_file}"],
            path=root,
            silent=True,
        )


def changeAppIcon(root, appIconPath):
    with open(f"{root}/loyalty2_0/flutter_launcher_icons-prod.yaml", "r") as file:
        data = file.read()
        actualIcon = data.split("image_path: ")[1].split("\n")[0]
        data = data.replace(f"image_path: {actualIcon}", f"image_path: {appIconPath}")
        with open(f"{root}/loyalty2_0/flutter_launcher_icons-prod.yaml", "w") as file:
            file.write(data)

    with open(f"{root}/loyalty2_0/ios/Runner.xcodeproj/project.pbxproj", "r") as file:
        data = file.read()
        run_command(
            [
                "dart",
                "run",
                "flutter_launcher_icons:main",
            ],
            path=f"{root}/loyalty2_0",
            silent=True,
        )
        with open(
            f"{root}/loyalty2_0/ios/Runner.xcodeproj/project.pbxproj", "w"
        ) as file:
            file.write(data)


def setupEnvFile(flavor, root):
    run_command(
        [
            "cp",
            f"{root}/loyalty2_0/envs/{flavor}.env",
            f"{root}/loyalty2_0/.env",
        ],
        path=root,
        silent=True,
    )
    run_command(
        [
            "dart",
            "run",
            "app_env",
        ],
        path=f"{root}/loyalty2_0",
        silent=True,
    )


def getEnv(flavor, root):
    with open(f"{root}/loyalty2_0/envs/{flavor}.env", "r") as file:
        data = file.read()
        bundleId = data.split("LOYALTY_APP_ID=")[1].split("\n")[0]
        print(f"Bundle ID: {bundleId}")
        appName = data.split("LOYALTY_APP_NAME_BUILD=")[1].split("\n")[0]
        print(f"App Name: {appName}")
        flavor = data.split("LOYALTY_APP_FLAVOR=")[1].split("\n")[0]
        print(f"Flavor: {flavor}")
        appIconPath = data.split("LOYALTY_PROJECT_ICON_PATH=")[1].split("\n")[0]
        print(f"App Icon Path: {appIconPath}")
    return flavor, bundleId, appName, appIconPath
