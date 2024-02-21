from distutils.core import setup

setup(
    name='kivy_remote_control',
    packages=['kivy_remote_control'],
    version='0.1', 
    license='MIT',
    description='Kivy android joystick for mavsdk',
    author='aj',
    author_email='aj@datainc.co.za',
    url='https://github.com/uberkie/kivy_remote_control',
    download_url='https://github.com/user/kivy_remote_control/archive/v_01.tar.gz',
    keywords=['kivy', 'mavlink', 'mavsdk', 'joystick', 'android'],
    install_requires=[
        'kivy',

    ],
    classifiers=[
        'Development Status :: 3 - Alpha',


        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
