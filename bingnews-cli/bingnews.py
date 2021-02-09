"""A command line interface to show the potential for finding news with the Bing News Search API."""
import os
import textwrap

import requests
import requests_cache
import pyshorteners

import click
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()
requests_cache.install_cache("bingsearch_cache", expire_after=300)
requests_cache.remove_expired_responses()


def clean_trending_article_dictionary(article_dictionary):
    """Take a dictionary for a trending article, and tweak the output."""
    source = article_dictionary["image"]["provider"][0]
    article_dictionary["title"] = article_dictionary["name"]
    article_dictionary["url"] = article_dictionary["webSearchUrl"]
    article_dictionary[
        "description"
    ] = f"Provided by {source['name']}, an {source['_type']}."
    return article_dictionary


def clean_bing_article_list(bing_article_list):
    """Take a list of articles, and clean the outputs."""
    cleaned_list = []
    shortener = pyshorteners.Shortener()
    for item in bing_article_list:
        if "name" in item and "webSearchUrl" in item:
            item = clean_trending_article_dictionary(item)
        new_dictionary = {
            "Title": "\n".join(textwrap.wrap(item["name"], width=40)),
            "Description": "\n".join(textwrap.wrap(item["description"], width=60)),
            "URL": shortener.qpsru.short(item["url"]),
        }
        cleaned_list.append(new_dictionary)
    return cleaned_list


def print_bing_results(bing_response_json):
    """Print out the results of the Bing News API output."""
    assert "value" in bing_response_json
    articles = bing_response_json["value"]
    cleaned_articles = clean_bing_article_list(articles)
    click.secho(
        tabulate(
            cleaned_articles,
            headers="keys",
            tablefmt="grid",
            colalign=["left", "left", "left"],
        )
    )
    if "totalEstimatedMatches" in bing_response_json:
        click.secho(f"{bing_response_json['totalEstimatedMatches']} estimated matches.")


def search_and_output_bing(query_string="", params=None):
    """Take the different variation of bing queries, and call the API."""
    if params is None:
        params = {}
    subscription_key = os.getenv("BING_SEARCH_KEY")
    assert subscription_key is not None
    bing_search_endpoint = os.getenv("BING_SEARCH_ENDPOINT")
    assert bing_search_endpoint is not None
    search_url = f"{bing_search_endpoint}v7.0/news{query_string}"
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    response = requests.get(search_url, headers=headers, params=params)
    try:
        response.raise_for_status()
        print_bing_results(response.json())
    except requests.exceptions.HTTPError as error:
        click.secho(f"Error: {str(error)}", fg="red")


@click.group()
def cli():
    """A CLI to search for news articles using Bing News, and return appropriate articles."""


@cli.command("phrase")
@click.option("-p", "--search_phrase", prompt="What phrase are you searching for?")
def search_bing_by_phrase(search_phrase):
    """Search Bing News by word or phrase."""
    params = {"q": search_phrase, "textDecorations": False}
    click.secho(f"Searching for {search_phrase}...")
    search_and_output_bing("/search", params)


@cli.command("cat")
@click.option(
    "-c",
    "--category",
    type=click.Choice(
        ["Business", "ScienceAndTechnology", "Sports", "World", "Entertainment"],
        case_sensitive=False,
    ),
    prompt=True,
)
@click.option(
    "-m",
    "--market",
    type=click.Choice(
        ["en-GB", "en-US"],
        case_sensitive=False,
    ),
    default="en-GB",
    show_default=True,
)
def search_bing_by_category(category="ScienceAndTechnology", market="en-GB"):
    """Search Bing News by category."""
    click.secho(f"Searching for {category} in {market}...")
    search_and_output_bing(f"?mkt={market}&category={category}")


@cli.command("trend")
@click.option(
    "-m",
    "--market",
    type=click.Choice(
        ["en-GB", "en-US"],
        case_sensitive=False,
    ),
    default="en-GB",
    show_default=True,
)
def search_bing_by_trending(market="en-GB"):
    """Search Bing News for trending topics."""
    click.secho(f"Searching for trending topics in {market}...")
    search_and_output_bing(f"/trendingtopics?mkt={market}")


if __name__ == "__main__":
    cli()
