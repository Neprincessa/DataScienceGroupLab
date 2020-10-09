package com.company;

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.ParserConfigurationException;

import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import org.xml.sax.SAXException;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Main {

    public static void main(String[] args) throws IOException {
        try {
            String csvFile = "C:\\Nina\\MEPHI\\8 семестр\\midterm_project\\Airlines\\PointzAggregator-AirlinesData.csv";
            FileWriter writer = new FileWriter(csvFile);
            CSVUtils.writeLine(writer, Collections.singletonList
                    ("uid;first;last;cards_type;card_number;bonusprogramm;activities_type;activity_type;code;date;departure;arrival;fare"));

            File fXmlFile = new File("C:\\Nina\\MEPHI\\8 семестр\\midterm_project\\Airlines\\PointzAggregator-AirlinesData.xml");
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(fXmlFile);

            List<String> firstPart = new ArrayList<String>();
            List<String> secondPart = new ArrayList<String>();
            List<String> thirdPart = new ArrayList<String>();
            List<String> row = new ArrayList<>();

            NodeList userList = doc.getElementsByTagName("user");

            for (int userID = 0; userID < userList.getLength(); userID++) {
                row.clear();

                Node user = userList.item(userID);
                if (user.getNodeType() == Node.ELEMENT_NODE) {
                    Element userElement = (Element) user;
                    firstPart.clear();
                    firstPart.add(userElement.getAttribute("uid"));

                    NodeList childNodesUser = user.getChildNodes();
                    for (int userChildID = 0; userChildID < childNodesUser.getLength(); userChildID++) {
                        Node userChild = childNodesUser.item(userChildID);
                        String nameUserChild = userChild.getNodeName();
                        if (nameUserChild.equals("name")) {
                            Element nameElement = (Element) userChild;
                            firstPart.add(nameElement.getAttribute("first"));
                            firstPart.add(nameElement.getAttribute("last"));
                        }
                        if (nameUserChild.equals("cards")) {
                            Element cardsElement = (Element) userChild;
                            firstPart.add(cardsElement.getAttribute("type"));

                            NodeList cardsList = userChild.getChildNodes();
                            if (cardsList.getLength() == 0) {
                                secondPart.clear();
                                thirdPart.clear();
                                for (int i = 0; i < 3; i++)
                                    secondPart.add("");
                                for (int i = 0; i < 6; i++)
                                    thirdPart.add("");

                                for (int i = 0; i < firstPart.size(); i++)
                                    row.add(firstPart.get(i));
                                for (int i = 0; i < secondPart.size(); i++)
                                    row.add(secondPart.get(i));
                                for (int i = 0; i < thirdPart.size(); i++)
                                    row.add(thirdPart.get(i));
                                CSVUtils.writeLine(writer, row);
                            } else {
                                for (int cardID = 0; cardID < cardsList.getLength(); cardID++) {
                                    secondPart.clear();
                                    Node card = cardsList.item(cardID);
                                    if (card.getNodeType() == Node.ELEMENT_NODE) {
                                        Element cardElement = (Element) card;
                                        secondPart.add(cardElement.getAttribute("number"));
                                        secondPart.add(cardElement.getElementsByTagName("bonusprogramm").item(0).getTextContent());

                                        NodeList childNodesCard = card.getChildNodes();
                                        for (int cardChildID = 0; cardChildID < childNodesCard.getLength(); cardChildID++) {
                                            Node cardChild = childNodesCard.item(cardChildID);
                                            String nameCardChild =  cardChild.getNodeName();
                                            if (nameCardChild.equals("activities")) {
                                                Element nameElement = (Element) cardChild;
                                                secondPart.add(nameElement.getAttribute("type"));

                                                NodeList activitiesList = cardChild.getChildNodes();
                                                if (activitiesList.getLength() == 0) {
                                                    thirdPart.clear();
                                                    for (int i = 0; i < 6; i++)
                                                        thirdPart.add("");
                                                    row.clear();
                                                    for (int i = 0; i < firstPart.size(); i++)
                                                        row.add(firstPart.get(i));
                                                    for (int i = 0; i < secondPart.size(); i++)
                                                        row.add(secondPart.get(i));
                                                    for (int i = 0; i < thirdPart.size(); i++)
                                                        row.add(thirdPart.get(i));
                                                    CSVUtils.writeLine(writer, row);
                                                } else {
                                                    for (int activityID = 0; activityID < activitiesList.getLength(); activityID++) {
                                                        thirdPart.clear();
                                                        Node activity = activitiesList.item(activityID);
                                                        if (activity.getNodeType() == Node.ELEMENT_NODE) {
                                                            Element activityElement = (Element) activity;
                                                            thirdPart.add(activityElement.getAttribute("type"));
                                                            thirdPart.add(activityElement.getElementsByTagName("Code").item(0).getTextContent());
                                                            thirdPart.add(activityElement.getElementsByTagName("Date").item(0).getTextContent());
                                                            thirdPart.add(activityElement.getElementsByTagName("Departure").item(0).getTextContent());
                                                            thirdPart.add(activityElement.getElementsByTagName("Arrival").item(0).getTextContent());
                                                            thirdPart.add(activityElement.getElementsByTagName("Fare").item(0).getTextContent());
                                                            row.clear();
                                                            for (int i = 0; i < firstPart.size(); i++)
                                                                row.add(firstPart.get(i));
                                                            for (int i = 0; i < secondPart.size(); i++)
                                                                row.add(secondPart.get(i));
                                                            for (int i = 0; i < thirdPart.size(); i++)
                                                                row.add(thirdPart.get(i));
                                                            CSVUtils.writeLine(writer, row);
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            writer.flush();
            writer.close();
        } catch (ParserConfigurationException e) {
            e.printStackTrace();
        } catch (SAXException e) {
            e.printStackTrace();
        }
    }
}