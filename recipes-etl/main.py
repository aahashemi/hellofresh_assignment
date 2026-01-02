from pathlib import Path
from dataset import RecipesDataset
from loguru import logger
import isodate

def parse_iso_duration(duration: str) -> int | None:

    if not isinstance(duration, str):
        return None

    if not duration or not duration.startswith("PT"):
        return None

    td = isodate.parse_duration(duration)
    return int(td.total_seconds() // 60)

def classify_difficulty(prepTime: str, cookTime: str) -> str:

    prep_min = parse_iso_duration(prepTime) or 0
    cook_min = parse_iso_duration(cookTime) or 0
    total = prep_min + cook_min

    if total > 60:
        return "Hard"
    elif total >= 30:
        return "Medium"
    elif total > 0:
        return "Easy"
    else:
        return "Unknown"

def main():

    dataset = RecipesDataset()
    df = dataset.get_dataset()
    
    # handles chili/chilies/chilli/chillies/chile/chiles
    chili_pattern = r"\bchill?i(?:es)?\b|\bchil?e(?:s)?\b" 

    df_chili = df[
        df["ingredients"].str.contains(
            chili_pattern, 
            regex=True, 
            case=False, 
            na=False
        )].drop_duplicates()
    
    df_chili["difficulty"] = df_chili.apply(
        lambda row: classify_difficulty(row.get("prepTime"), row.get("cookTime")),
        axis=1
    )

    output_file = Path(__file__).parent / "chilies_recipes.csv"

    logger.info(f"Saving chilies recipes to {output_file}")
    df_chili.to_csv(output_file, index=False)
    
    
    
if __name__ == "__main__":
    main()
