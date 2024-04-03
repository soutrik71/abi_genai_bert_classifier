import logging

from sklearn.model_selection import train_test_split

from src.settings import LoggerSettings

logger = logging.getLogger(LoggerSettings().logger_name)


def data_preprocess(data, evaluation_size, seed):
    """Preprocess data for training and evaluation"""
    # Normalization of labels
    data["FinalLabel"] = (
        data["FinalLabel"].apply(lambda x: x.upper()).map({"SIMPLE": 0, "COMPLEX": 1})
    )
    data["FinalLabel"] = data["FinalLabel"].astype(int)

    # startified train test split
    train_df, test_df = train_test_split(
        data,
        test_size=evaluation_size,
        random_state=seed,
        stratify=data["FinalLabel"],
    )
    logger.info(
        f"Train and test dataframes created with {evaluation_size} with sizes {train_df.shape} and {test_df.shape}"
    )
    logger.info(
        f'proportion of targets in train is {train_df["FinalLabel"].value_counts()/len(train_df)} and in test is {test_df["FinalLabel"].value_counts()/len(test_df)}'
    )

    return train_df, test_df
