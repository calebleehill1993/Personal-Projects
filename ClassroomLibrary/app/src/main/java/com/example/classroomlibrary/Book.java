package com.example.classroomlibrary;

import java.util.Scanner;

public class Book {
    private String title;
    private String author;
    private String series;
    private int numberInSeries;
    private String teacher;
    private String condition;
    private boolean checkedOut;
    private String isbn;
    private String genre;
    private double readingLevel;
    private boolean specialCollections;
    private String notes;

    public Book(String genre, String series, String numberInSeries, String author,
                String title, String readingLevel, String condition, String teacher,
                String specialCollections, String notes) {
        this.genre = genre;
        this.series = series;
        if (numberInSeries == "") {
            this.numberInSeries = 0;
        }
        else {
            this.numberInSeries = Integer.parseInt(numberInSeries);
        }
        this.author = author;
        this.title = title;
        if (readingLevel == "") {
            this.readingLevel = 0;
        }
        else {
            this.readingLevel = Double.parseDouble(readingLevel);
        }
        this.condition = condition;
        this.teacher = teacher;
        if (specialCollections.toUpperCase() == "TRUE") {
            this.specialCollections = true;
        }
        else {
            this.specialCollections = false;
        }
        this.notes = notes;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public void setSeries(String series) {
        this.series = series;
    }

    public void setNumberInSeries(int numberInSeries) {
        this.numberInSeries = numberInSeries;
    }

    public void setTeacher(String teacher) {
        this.teacher = teacher;
    }

    public void setCondition(String condition) {
        this.condition = condition;
    }

    public void setCheckedOut(boolean checkedOut) {
        this.checkedOut = checkedOut;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }

    public void setGenre(String genre) {
        this.genre = genre;
    }

    public void setReadingLevel(double readingLevel) {
        this.readingLevel = readingLevel;
    }

    public void setSpecialCollections(boolean specialCollections) {
        this.specialCollections = specialCollections;
    }

    public void setNotes(String notes) {
        this.notes = notes;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }

    public String getSeries() {
        return series;
    }

    public int getNumberInSeries() {
        return numberInSeries;
    }

    public String getTeacher() {
        return teacher;
    }

    public String getCondition() {
        return condition;
    }

    public boolean isCheckedOut() {
        return checkedOut;
    }

    public String getIsbn() {
        return isbn;
    }

    public String getGenre() {
        return genre;
    }

    public double getReadingLevel() {
        return readingLevel;
    }

    public boolean isSpecialCollections() {
        return specialCollections;
    }

    public String getNotes() {
        return notes;
    }

    public static void main(String[] args) {

    }

}
