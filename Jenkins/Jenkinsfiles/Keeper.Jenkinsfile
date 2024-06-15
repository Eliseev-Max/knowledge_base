pipeline {
    agent {
        dockerfile {
            filename "docker/test/Dockerfile"
            additionalBuildArgs "--label built-by-jenkins"
            args "--network=host"
        }
    }

    triggers {
        cron(env.BRANCH_NAME.equals("master") ? "H H(19-22) * * *" : "")
    }

    parameters {
        choice(
            name: "MAKE_JOBS",
            choices: [ "4", "1", "2", "4", "8", "16", "32" ],
            description: "Количество потоков Make."
        )
        choice(
            name: "CLANG_TIDY_JOBS",
            choices: [ "4", "1", "2", "8", "16", "32" ],
            description: "Количество потоков Clang-Tidy."
        )
        booleanParam(
            name: "CPPCHECK",
            defaultValue: true,
            description: "Включить проверку Cppcheck."
        )
        booleanParam(
            name: "CLANG_TIDY",
            defaultValue: false,
            description: "Включить проверку Clang-Tidy."
        )
        booleanParam(
            name: "UNIT_TESTS",
            defaultValue: true,
            description: "Включить сборку и выполнение тестов."
        )
        booleanParam(
            name: "COVERAGE",
            defaultValue: true,
            description: "Включить проверку покрытия кода."
        )
        booleanParam(
            name: "FUZZING",
            defaultValue: true,
            description: "Включить фаззинг-тестирование кода."
        )
        choice(
            name: "FUZZING_TIME_LIMIT",
            choices: [ "30", "60", "120", "180" ],
            description: "Количество секунд выделенных на выполнение одного фаззинг-теста."
        )
        booleanParam(
            name: "DOXYGEN",
            defaultValue: true,
            description: "Включить генерацию документации Doxygen."
        )
    }

    stages {
        stage("Configuration") {
            steps {
                sh "rm -rf ./build"
                sh "cmake -B ./build --preset 'unit-tests'"
            }
        }
        stage("Cppcheck") {
            when { expression { params.CPPCHECK } }
            steps {
                sh "cmake --build ./build --target cppcheck"
            }
        }
        stage("Clang-Tidy") {
            when { expression { params.CLANG_TIDY } }
            steps {
                sh "cmake -B ./build -DKPR_CLANG_TIDY_JOBS=${params.CLANG_TIDY_JOBS}"
                sh "cmake --build ./build --target clang-tidy"
            }
        }
        stage("SonarQube") {
            when {
                allOf {
                    branch "master"
                    expression { params.CPPCHECK }
                }
            }
            stages {
                stage("SonarScanner") {
                    steps {
                        withSonarQubeEnv("SonarQube Server") {
                            sh """
                                ${tool 'SonarScanner'}/bin/sonar-scanner \
                                    -Dsonar.cxx.cppcheck.reportPaths=build/cppcheck/err.xml \
                                    -Dsonar.cfamily.compile-commands=build/compile_commands.json
                            """
                        }
                    }
                }
                stage("Quality Gate") {
                    steps {
                        timeout(time: 1, unit: 'HOURS') {
                            waitForQualityGate abortPipeline: true
                        }
                    }
                }
            }
        }
        stage("Unit Tests") {
            when { expression { params.UNIT_TESTS } }
            steps {
                script {
                    if (params.COVERAGE) {
                        sh "cmake -B ./build -DKPR_COVERAGE_ENABLED=ON"
                    }
                }
                sh "cmake --build ./build -j ${params.MAKE_JOBS}"
                sh "ctest --test-dir ./build --preset 'ci'"
            }
            post {
                always { junit "build/output-junit.xml" }
            }
        }
        stage("Report Coverage") {
            when {
                allOf {
                    expression { params.UNIT_TESTS }
                    expression { params.COVERAGE }
                }
            }
            steps {
                sh "cmake --build ./build --target coverage-xml"
            }
            post {
                success {
                    cobertura(
                        autoUpdateHealth: false,
                        autoUpdateStability: false,
                        coberturaReportFile: "build/coverage.xml",
                        conditionalCoverageTargets: "70, 0, 0",
                        failUnhealthy: false,
                        failUnstable: false,
                        lineCoverageTargets: "80, 0, 0",
                        maxNumberOfBuilds: 0,
                        methodCoverageTargets: "80, 0, 0",
                        onlyStable: false,
                        sourceEncoding: "UTF_8",
                        zoomCoverageChart: false
                    )
                }
            }
        }
        stage("Fuzzing") {
            when { expression { params.FUZZING } }
            steps {
                sh "rm -rf ./build"
                sh "cmake -B ./build --preset 'fuzzing'"
                sh "cmake -B ./build -DKPR_FUZZING_TIME_LIMIT=${params.FUZZING_TIME_LIMIT}"
                sh "cmake --build ./build --target fuzzer -j ${params.MAKE_JOBS}"
                sh "cmake --build ./build --target fuzzer_coverage"
            }
            post {
                success {
                    publishHTML(
                        target: [
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: false,
                            reportDir: "build/fuzzer_coverage-html",
                            reportFiles: "index.html",
                            reportName: "Fuzzing Coverage Report"
                         ]
                     )
                }
            }
        }
        stage("Doxygen") {
            when { expression { params.DOXYGEN } }
            steps {
                sh "cmake --build ./build --target doxygen"
            }
            post {
                success {
                    publishHTML(
                        target: [
                            allowMissing: false,
                            alwaysLinkToLastBuild: true,
                            keepAll: false,
                            reportDir: "docs/html",
                            reportFiles: "index.html",
                            reportName: "Doxygen Documentation"
                         ]
                     )
                }
            }
        }
    }
}

