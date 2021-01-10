import random
import threading
from typing import List

import requests
import json


class Client:
    def __init__(self):
        self.__root = "http://localhost:8080/"

    def getAllShows(self) -> List[list]:
        response = requests.get(self.__root + "concert/all")
        showsList = json.loads(response.text)
        idShows = [[show["idShow"], show["hall"]] for show in showsList]
        return idShows

    def getHallSeats(self, hallId: int) -> int:
        response = requests.get(self.__root + "hall/getOne/?id=" + str(hallId))
        hall = json.loads(response.text)
        return hall["nrSeats"]

    def postSale(self, idShow: int, noOfSeats: int, seats: List[int]):
        seatsString = ""
        for i in seats:
            seatsString = seatsString + "&seat=" + str(i)
        response = requests.post(
            self.__root + "/sale/add?concert=" + str(idShow) + "&num=" + str(noOfSeats) + seatsString)
        print(response.text)

    def makeSale(self):
        showsList = self.getAllShows()
        show = random.choice(showsList)
        hallSeats = self.getHallSeats(show[1])
        noOfSeats = random.randint(1, 10)
        seats = random.sample(range(1, hallSeats), noOfSeats)
        self.postSale(show[0], noOfSeats, seats)
        print("am trecut")

    def start(self):
        t = threading.Timer(2.0, self.start)

        try:
            self.makeSale()
        except:
            t.cancel()
            print("server inchis")
        t.start()



if __name__ == '__main__':
    client = Client()
    client.start()
