package org.isaqb.asciidoc;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Locale;
import org.asciidoctor.Asciidoctor;
import org.asciidoctor.Attributes;
import org.asciidoctor.Options;
import org.asciidoctor.SafeMode;

import java.io.File;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Stream;

import static org.asciidoctor.Asciidoctor.Factory.create;

public final class Main {

  private static final String PROJECT_VERSION = "projectVersion";
  private static final String CURRICULUM_FILE_NAME = "curriculumFileName";
  private static final String INDEX_FILE_NAME = "index";
  private static final String VERSION_DATE = "versionDate";
  private static final String VALIDITY = "validity";
  private static final String LANGUAGES = "languages";
  private static final String[] FORMATS = {"html", "pdf"};

  private static final String LANGUAGE_SEPERATOR = ",";

  private static final String SOURCE_DIR = "./docs/";
  private static final String BASE_DIR = SOURCE_DIR;
  private static final String OUTPUT_DIR = "./build/";

  private static final String ADOC = "adoc";
  private static final String HTML = "html";
  private static final String HTML5 = "html5";
  private static final String PDF = "pdf";
  private static final String ENGLISH = "EN";
  private static final String GERMAN = "DE";

  private Main() {
  }

  public static void main(final String[] args) {
    Objects.requireNonNull(System.getProperty(PROJECT_VERSION));
    Objects.requireNonNull(System.getProperty(CURRICULUM_FILE_NAME));
    Objects.requireNonNull(System.getProperty(VERSION_DATE));
    Objects.requireNonNull(System.getProperty(LANGUAGES));
    Objects.requireNonNull(System.getProperty(VALIDITY));

    final String projectVersion = System.getProperty(PROJECT_VERSION);
    final String curriculumFileName = System.getProperty(CURRICULUM_FILE_NAME);
    final String versionDate = System.getProperty(VERSION_DATE);
    final String[] languages = System.getProperty(LANGUAGES).split(LANGUAGE_SEPERATOR);
    final String validity = System.getProperty(VALIDITY);

    Stream.of(languages).forEach(language -> convertInLanguage(
        language,
        projectVersion,
        curriculumFileName,
        versionDate,
        validity,
        curriculumFileName
    ));

    convertInFormat(HTML,
        projectVersion,
        INDEX_FILE_NAME,
        versionDate,
        null,
        ENGLISH,
        curriculumFileName);
  }

  private static void convertInLanguage(
      final String language,
      final String projectVersion,
      final String curriculumFileName,
      final String versionDate,
      final String validity,
      final String curriculumName) {
    Stream.of(FORMATS).forEach(format -> convertInFormat(
        format, projectVersion,
        curriculumFileName,
        versionDate,
        validity,
        language,
        curriculumName
    ));
  }

  private static void convertInFormat(
      final String format,
      final String projectVersion,
      final String curriculumFileName,
      final String versionDate,
      final String validity,
      final String language,
      final String curriculumName) {
    try (final Asciidoctor asciidoctor = create()) {
      final Attributes attributes = toAttributes(
          projectVersion,
          curriculumName,
          versionDate,
          validity,
          language);

      asciidoctor.convertDirectory(
          List.of(new File("%s%s.%s".formatted(
              SOURCE_DIR,
              curriculumFileName,
              ADOC))),
          Options.builder()
              .baseDir(new File(BASE_DIR))
              .backend(toBackend(format))
              .mkDirs(true)
              .attributes(attributes)
              .standalone(true)
              .toDir(new File(OUTPUT_DIR))
              .safe(SafeMode.UNSAFE)
              .build());

      if (!INDEX_FILE_NAME.equals(curriculumFileName)) {
        // rename only if we're not creating the index file.
        renameResultAccordingToLanguage(curriculumFileName, format, language);
      }
    }
  }

  private static Attributes toAttributes(
      final String projectVersion,
      final String curriculumFileName,
      final String versionDate,
      final String validity,
      final String language) {
    final String fileVersion = "%s-%s".formatted(projectVersion, language);
    final String documentVersion = "%s-%s (%s)".formatted(fileVersion, versionDate, formatValidity(validity, language));

    final Map<String, Object> attributes = new HashMap<>() {{
      put("icons", "font");
      put("version-label", "");
      put("release-version", projectVersion);
      put("revnumber", fileVersion);
      put("revdate", versionDate);
      put("document-version", documentVersion);
      put("currentDate", versionDate);
      put("language", language);
      put("curriculumFileName", curriculumFileName);
      put("pdf-themesdir", "../pdf-theme/themes");
      put("pdf-fontsdir", "../pdf-theme/fonts");
      put("pdf-theme", "isaqb");
      put("stylesheet", "../html-theme/adoc-github.css");
      put("stylesheet-dir", "../html-theme");
      put("data-uri", true);
      put("allow-uri-read", true);
    }};

    return Attributes.builder().attributes(attributes).build();
  }

  private static String formatValidity(final String validity, final String language) {
    String validityFormatted;
    try {

      if (validity == null) {
        validityFormatted = "";
      } else if (ENGLISH.equals(language)) {
        validityFormatted =
            "valid from " + new SimpleDateFormat("MMMM d, yyyy", Locale.US).format(
                new SimpleDateFormat("yyyy/MM/dd", Locale.US).parse(
                    validity));
      } else {
        validityFormatted =
            "Gültig ab " + new SimpleDateFormat("d. MMMM yyy", Locale.GERMANY).format(
                new SimpleDateFormat("yyyy/MM/dd", Locale.US).parse(
                    validity));
      }
    } catch (final ParseException e) {
      validityFormatted = "";
    }

    return validityFormatted;
  }

  private static String toBackend(final String format) {
    return switch (format) {
      case HTML -> HTML5;
      case PDF -> PDF;
      default -> throw new IllegalArgumentException("Unknown target format %s".formatted(format));
    };
  }

  private static void renameResultAccordingToLanguage(
      final String fileName,
      final String format,
      final String language) {
    final File original = new File("%s%s.%s".formatted(OUTPUT_DIR, fileName, format));
    final File renamed = new File(
        "%s%s-%s.%s".formatted(OUTPUT_DIR, fileName, language.toLowerCase(), format));
    if (!original.exists()) {
      System.err.printf("Failed to rename result file %s as it does not exist",
          original.getAbsolutePath());
    } else if (!original.renameTo(renamed)) {
      System.err.printf("Failed to rename result file %s to %s%n", original.getName(),
          renamed.getName());
    }
    original.deleteOnExit();
  }
}
