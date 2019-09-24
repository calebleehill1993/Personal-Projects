package com.example.classroomlibrary;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class Import {
    public static List main(String importFile) throws Exception {
        File file = new File("//home//caleb//Downloads//" + importFile);
        BufferedReader br = new BufferedReader(new FileReader(file));
        String st;
        List<String> things = new ArrayList<>();
        while ((st = br.readLine()) != null) {
            String temp = "";
            st = st + "\t";
            for (int i = 0; i < 10; i++){
                while (st.charAt(0) != '\t') {
                    temp = temp + st.charAt(0);
                    st = st.substring(1);
                }
                st = st.substring(1);
                things.add(temp);
                temp = "";
            }

        }
        List<Book> classLibrary = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            things.remove(0);
        }
        System.out.print(things);
        while (things.size() > 0) {
            classLibrary.add(new Book(things.get(0), things.get(1), things.get(2),
                    things.get(3), things.get(4), things.get(5), things.get(6),
                    things.get(7), things.get(8), things.get(9)));
            for (int i = 0; i < 10; i++) {
                things.remove(0);
            }
        }
        return classLibrary;
    }
}