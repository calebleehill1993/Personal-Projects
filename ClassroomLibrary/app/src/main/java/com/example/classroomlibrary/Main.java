package com.example.classroomlibrary;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class Main {
    ArrayList classLibrary;

    public static void main(String[] args) throws Exception {
        Main myMain = new Main();
        List<Book> classroomLibrary = new ArrayList<>();
        classroomLibrary = Import.main("ClassroomLibrary.tsv");
        for (int i = 0; i < classroomLibrary.size(); i++) {
            System.out.println(classroomLibrary.get(i).getTitle());
        }
    }

    public void addBook() {
        Scanner in = new Scanner(System.in);
        System.out.print("Title: ");
        String title = in.nextLine();
        System.out.print("Author: ");
        String author = in.nextLine();
        System.out.print("ISBN: ");
        String isbn = in.nextLine();
        System.out.print("Series: ");
        String series = in.nextLine();
        System.out.print("Teacher: ");
        String teacher = in.nextLine();
        System.out.print("Condition: ");
        String condition = in.nextLine();
        return;
    }
}
