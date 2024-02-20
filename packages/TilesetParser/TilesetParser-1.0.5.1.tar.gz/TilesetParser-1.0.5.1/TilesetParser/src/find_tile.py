import cv2
import os
from .gui import show_images
from skimage.metrics import structural_similarity as ssim


def compare_images(img1, img2):
    hist1 = cv2.calcHist([img1], [0], None, [256], [0, 256])
    hist2 = cv2.calcHist([img2], [0], None, [256], [0, 256])
    score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
    return score


def split_into_tiles(image, tile_size):
    tiles = []
    for y in range(0, image.shape[0], tile_size[1]):
        for x in range(0, image.shape[1], tile_size[0]):
            tile = image[y:y+tile_size[1], x:x+tile_size[0]]
            tiles.append(tile)
    return tiles


def remove_duplicates_by_name(objects):
    unique = {}
    for obj in objects:
        if obj['file'] not in unique:
            unique[obj['file']] = obj
    return list(unique.values())


def find_matching_tile(source_image_path, tiles_folder, tile_size, similarity, extension, tiles_per_tileset):
    source_image = cv2.imread(source_image_path, cv2.IMREAD_COLOR)
    assert source_image.shape[:2] == (
        tile_size, tile_size), f"Source image must be {tile_size}px x {tile_size}px"

    results = []

    for root, dirs, files in os.walk(tiles_folder):
        for file in files:
            if file.endswith(f".{extension}"):
                tile_path = os.path.join(root, file)
                tile_image = cv2.imread(tile_path, cv2.IMREAD_COLOR)

                tiles = split_into_tiles(
                    tile_image, tile_size=(tile_size, tile_size))

                for i, tile in enumerate(tiles):
                    if tile.shape[:2] == (tile_size, tile_size):
                        row = i // tiles_per_tileset
                        col = i % tiles_per_tileset
                        print(
                            f" Current file: {file} | Current row: {row} | Current column: {col}")
                        score = compare_images(source_image, tile)
                        if score >= similarity:
                            result_object = {
                                "file": tile_path,
                                "input_tile": source_image_path,
                                "similarity": f"{'{:.2f}'.format(score * 100)}%"
                            }
                            if result_object not in results:
                                results.append(result_object)
                            print(
                                f"Tile was found at: {tile_path} | position: (row: {row}, col: {col}) | Similarity level: {'{:.2f}'.format(score * 100)}%")
        tiles_list = sorted(remove_duplicates_by_name(results), key=lambda x: float(
            x['similarity'].rstrip('%')), reverse=True)
        print(tiles_list)
        return show_images(tiles_list)

    print("Tile not found.")
    return None, None


def find_matching_tile_ssim(source_image_path, tiles_folder, tile_size, similarity, extension):
    source_image = cv2.imread(source_image_path, cv2.IMREAD_COLOR)
    assert source_image.shape[:2] == (
        tile_size, tile_size),  f"Source image must be {tile_size}px x {tile_size}px"

    results = []

    for root, dirs, files in os.walk(tiles_folder):
        for file in files:
            if file.endswith(f".{extension}"):
                tile_path = os.path.join(root, file)
                tile_image = cv2.imread(tile_path, cv2.IMREAD_COLOR)

                tiles = split_into_tiles(
                    tile_image, tile_size=(tile_size, tile_size))

                for tile in tiles:
                    ssim_score = calculate_ssim(source_image, tile)
                    print(
                        f" Current file: {file} | ssim_score: {'{:.2f}'.format(ssim_score * 100)}%")
                    if ssim_score >= (similarity):
                        result_object = {
                            "file": tile_path,
                            "input_tile": source_image_path,
                            "similarity": f"{'{:.2f}'.format(ssim_score * 100)}%"
                        }

                        if result_object not in results:
                            results.append(result_object)
                            print(
                                f"Tile was found at: {tile_path} | Similarity level: {'{:.2f}'.format(ssim_score * 100)}%")
        tiles_list = sorted(remove_duplicates_by_name(results), key=lambda x: float(
            x['similarity'].rstrip('%')), reverse=True)
        print(tiles_list)
        return show_images(tiles_list)

    print("Tile not found.")
    return None, None


def calculate_ssim(img1, img2):
    win_size = 3
    ssim_score = ssim(img1, img2, win_size=win_size, multichannel=True)
    score = ssim_score * 2.3
    if int('{:.2f}'.format(score * 100)) > 100:
        score = 1.00
    return score
