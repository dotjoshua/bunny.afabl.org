lazy val commonSettings = Seq(
  version := "0.3.0",
  scalaVersion := "2.11.8",
  crossScalaVersions := Seq("2.11.7"),
  organization := "org.afabl"
)

lazy val root = (project in file(".")).
  settings(commonSettings: _*).
  settings(
    name := "afabl-study",
    libraryDependencies ++= Seq(
      "ch.qos.logback" %  "logback-classic" % "1.1.7",
      "com.typesafe.scala-logging" %% "scala-logging" % "3.4.0"
    )
  )
