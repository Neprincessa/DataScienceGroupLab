package com.example.yamlparser

import android.app.Activity
import android.content.Intent
import android.net.Uri
import android.os.Bundle
import android.os.ParcelFileDescriptor
import android.provider.DocumentsContract
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import org.apache.commons.csv.CSVFormat
import org.apache.commons.csv.CSVParser
import org.apache.commons.csv.CSVPrinter
import org.yaml.snakeyaml.Yaml
import java.io.*
import java.nio.file.Files
import java.nio.file.Paths
import java.util.regex.Pattern


class MainActivity : AppCompatActivity() {

    private var txtview : TextView? = null
    private var file : File? = null
    private var uriyaml : Uri? = null
    private var reg : String = "\\'[12][0-9][0-9][0-9]-[01][0-9]-[0-3][0-9]\\':"
    private var reg2 : String = "[A-Z][A-Z][0-9][0-9][0-9][0-9]:"
    private val lineList = mutableListOf<String>()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val buttonFind : Button = findViewById(R.id.button)
        val buttonStart : Button = findViewById(R.id.button2)
        val buttonParse : Button = findViewById(R.id.button3)
        txtview = findViewById(R.id.textView)

        val contentResolver = applicationContext.contentResolver

        val takeFlags: Int = Intent.FLAG_GRANT_READ_URI_PERMISSION or
                Intent.FLAG_GRANT_WRITE_URI_PERMISSION
// Check for the freshest data.




        buttonFind.setOnClickListener {
            // Choose a directory using the system's file picker.
            val intent = Intent(Intent.ACTION_OPEN_DOCUMENT).apply {
                addCategory(Intent.CATEGORY_OPENABLE)
                type = "*/*"
                // Provide read access to files and sub-directories in the user-selected
                // directory.
                flags = Intent.FLAG_GRANT_READ_URI_PERMISSION or Intent.FLAG_GRANT_WRITE_URI_PERMISSION

                // Optionally, specify a URI for the directory that should be opened in
                // the system file picker when it loads.
                putExtra(DocumentsContract.EXTRA_INITIAL_URI, '/')
            }

            startActivityForResult(intent, 777)
//            val intent = Intent()
//                .setType("*/*")
//                .setAction(Intent.ACTION_GET_CONTENT)
//
//            startActivityForResult(Intent.createChooser(intent, "Select a file"), 777)
        }

        buttonStart.setOnClickListener {

            try {
                var index : Int = 0
                val fileName = "new1.yml"
                val parcelFileDescriptor: ParcelFileDescriptor? =
                    contentResolver.openFileDescriptor(uriyaml!!, "r")
                val fileDescriptor: FileDescriptor = parcelFileDescriptor!!.fileDescriptor
                val istream: FileInputStream? = FileInputStream(fileDescriptor)
                var index2 = 0

                var prevDate : String = ""

                istream?.bufferedReader()?.useLines {
                        lines -> lines.forEach {
                        var flag : Boolean = Pattern.matches(reg, it)
                        if (flag)
                        {
                            inputInfile(index, index2, lineList)
                            index += 1
                            index2 = 0
                            lineList.clear()
                            lineList.add(it)
                            prevDate = it
                            println(it)
                        }
                        else
                        {
                            val flag2 : Boolean = Pattern.matches(reg2, it.trim())
                            if(flag2 && index2 > 10)
                            {
                                inputInfile(index, index2, lineList)
                                lineList.clear()
                                lineList.add(prevDate)
                                index2 = 0
                            }
                            lineList.add(it)
                            index2 += 1
                        }
                    }
                }
                inputInfile(index, index2, lineList)


            }
            catch (e: IOException)
            {
                println("can't open file")
            }
        }

        buttonParse.setOnClickListener {
            val dir = File(this.getExternalFilesDir(null)?.toURI())
            val list = mutableListOf<String>()
            dir.walk().forEach { f ->
                if(f.isFile) {
                    list.add(f.name)
                } else {
                    println("dir ${f.name}")
                }
            }
            val yaml = Yaml()
            val path = this.getExternalFilesDir(null)

            val nFileCSV = File(path, "OutCSV.csv")
            val writer = Files.newBufferedWriter(Paths.get(nFileCSV.toURI()))
            val csvParser = CSVPrinter(writer, CSVFormat.DEFAULT)

            for(i in list)
            {
                val nFile = File(path, i)
                val inputStream = nFile.inputStream()
                val obj: Map<String, Any> = yaml.load(inputStream)
                var date = obj.keys.toList()
                val listData = kotlin.collections.mutableListOf<Any>()
                listData.add(date[0])
                val castobj :  Map<Any, Any>? = obj[date[0]] as Map<Any, Any>

                if (castobj != null) {
                    for(key in castobj) {
                        val value : Map<Any, Any>? = castobj[key.key] as Map<Any, Any>
                        val listData1 = kotlin.collections.mutableListOf<Any>()
                        listData1.add(date[0])
                        listData1.add(key.key)
                        value?.get("FROM")?.let { it1 -> listData1.add(it1) }
                        value?.get("STATUS")?.let { it1 -> listData1.add(it1) }
                        value?.get("TO")?.let { it1 -> listData1.add(it1) }
                        val value2 : Map<Any, Any>? = value?.get("FF") as Map<Any, Any>
                        if (value2 != null) {
                            for(key2 in value2) {
                                val value3 : Map<Any, Any>? = value2[key2.key] as Map<Any, Any>
                                val listData2 = kotlin.collections.mutableListOf<Any>()
                                val listData21 = kotlin.collections.mutableListOf<Any>()
                                listData21.add(key2.key)
                                value3?.get("CLASS")?.let { it -> listData21.add(it) }
                                value3?.get("FARE")?.let { it -> listData21.add(it) }

                                listData2.add(listData21)

                                for(j in listData2) {
                                    var listData3 = kotlin.collections.mutableListOf<Any>()
                                    listData3.addAll(listData1)
                                    listData3.addAll(j as Collection<Any>)
                                    csvParser.printRecord(listData3)
                                }
                            }
                        }
                    }
                }
                inputStream.close()
            }

            csvParser.flush()
            csvParser.close()
        }
    }

    fun inputInfile(index : Int, index2 : Int, list : List<String>) {

//        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.WRITE_EXTERNAL_STORAGE)
//            != PackageManager.PERMISSION_GRANTED) {
//            ActivityCompat.requestPermissions(this,
//                arrayOf(android.Manifest.permission.WRITE_EXTERNAL_STORAGE),
//                PackageManager.PERMISSION_GRANTED)
//        }

        val newName = "file$index$index2.yml"
        var Urisbstr = uriyaml.toString().substring(0, uriyaml.toString().length - "SkyTeam-Exchange.yaml".length) + newName
        val URInew = Uri.parse(Urisbstr)

        try {
            val path = this.getExternalFilesDir(null)
            val nFile = File(path, newName)

            for (i in list)
            {
                nFile.appendText(i)
                nFile.appendText("\n")
            }

//            nFile.bufferedWriter().use { out ->
//                for (i in list)
//                {
//                    out.write(i)
//                    out.write("\n")
//                }
//            }
        }
        catch (e: IOException)
        {
            println("can't open file")
        }





//        val intent = Intent(Intent.ACTION_CREATE_DOCUMENT).apply {
//            addCategory(Intent.CATEGORY_OPENABLE)
//            type = "*/*"
//            putExtra(Intent.EXTRA_TITLE, newName)
//
//            // Optionally, specify a URI for the directory that should be opened in
//            // the system file picker before your app creates the document.
//            putExtra(DocumentsContract.EXTRA_INITIAL_URI, URInew)
//        }
//        startActivityForResult(intent, 1)
//        sleep(5000)

//        val contentResolver = applicationContext.contentResolver
//        val takeFlags: Int = Intent.FLAG_GRANT_READ_URI_PERMISSION or
//                Intent.FLAG_GRANT_WRITE_URI_PERMISSION
//
//
//        if (URInew != null)
//        {
//            contentResolver.takePersistableUriPermission(URInew, takeFlags)
//        }



    }

    fun WriteInFile(URInew : Uri)
    {
        val parcelFileDescriptor: ParcelFileDescriptor? =
            contentResolver.openFileDescriptor(URInew, "w")
        val fileDescriptor: FileDescriptor = parcelFileDescriptor!!.fileDescriptor
        val outstream: FileOutputStream? = FileOutputStream(fileDescriptor)

        outstream?.bufferedWriter()?.use {out ->
            for (i in lineList) {
                out.write(i)
            }
        }
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, resultData: Intent?) {
        super.onActivityResult(requestCode, resultCode, resultData)

        if (requestCode == 777 && resultCode == Activity.RESULT_OK) {
            file = File(resultData?.data?.path.toString())
            txtview?.text = resultData?.data.toString()

            if (resultData != null)
            {
                val contentResolver = applicationContext.contentResolver
                val takeFlags: Int = Intent.FLAG_GRANT_READ_URI_PERMISSION or
                        Intent.FLAG_GRANT_WRITE_URI_PERMISSION

                if (resultData.data != null)
                {
                    contentResolver.takePersistableUriPermission(resultData.data!!, takeFlags)
                    uriyaml = resultData.data!!
                }

            }

        }
        if (requestCode == 1 && resultCode == Activity.RESULT_OK) {
            WriteInFile(resultData?.data!!)
        }
    }
}




