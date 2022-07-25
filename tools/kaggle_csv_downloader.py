def download_kaggle_dataset_to_colab_instance(api_command_from_kaggle: str, json_content: str) -> None:
    """
    descarga un dataset de la base de datasets de kaggle y lo guarda en la instancia de google colab activa.

    args:
        api_command_from_kaggle: es la linea de api que genera kaggle sobre el dataset, se consigue en las opciones del dataset.
        json_content: es el contenido del json que genera Kaggle cuando se genera una API TOKEN.

    """
    from zipfile import ZipFile
    ! pip install kaggle
    ! mkdir /root/.kaggle/
    with open("/root/.kaggle/kaggle.json", "w") as token:
        token.write(json_content)
    ! chmod 600 /root/.kaggle/kaggle.json
    ! kaggle config path -p /root/.kaggle/
    ! $api_command_from_kaggle
    name = f"{api_command_from_kaggle.split('/')[-1]}.zip"
    zip_ref = ZipFile(f"/content/{name}")
    zip_ref.extractall()
    zip_ref.close()
    ! rm $name

# download_kaggle_dataset_to_colab_instance("kaggle datasets download -d ccollado7/alternative-energies-argentina", '{"username":"charlymolero","key":"1d6b921759c70f37b628bb3d636a143a"}')