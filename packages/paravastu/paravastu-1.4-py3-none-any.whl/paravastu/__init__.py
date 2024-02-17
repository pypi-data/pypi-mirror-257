from biopandas.pdb import PandasPdb
import pandas
import numpy as np
from numpy.polynomial.polynomial import polyfit
from amino_info.py import *
import glob
import os
import ipywidgets
from IPython.display import display
import sys
from scipy.spatial.distance import cdist, pdist
from matplotlib import rcParams
import matplotlib.pyplot as plt
from itertools import combinations
from itertools import combinations_with_replacement
from pathlib import Path

labmodule = __import__(__name__)


def read_pdb(pdb_file):
    dataframe = pandas.DataFrame(PandasPdb().read_pdb(pdb_file).df["ATOM"])
    file = open(pdb_file, "r")
    text = file.readlines()
    file.close()
    dataframe.text = text
    dataframe.path = pdb_file
    return dataframe


def read_fplc(fplc_file):
    dataframe = pandas.read_csv(fplc_file, sep="\t", encoding="UTF-16")
    return dataframe


def get_atom(pdb_dataframe, segment_id, residue_num, atom_name):
    dataframe = pdb_dataframe.loc[pdb_dataframe["segment_id"] == segment_id]
    dataframe = dataframe.loc[pdb_dataframe["residue_number"] == residue_num]
    dataframe = dataframe.loc[pdb_dataframe["atom_name"] == atom_name]
    dataframe = dataframe[["x_coord", "y_coord", "z_coord"]]
    return dataframe.to_numpy()


def get_segments(pdb_dataframe):
    segment_set = PDBDataFrame.segment_id.unique()
    return segment_set


def euclidean_distance(coords1, coords2):
    return np.linalg.norm(coords1 - coords2)


def convert_to_one_letter(sequence, custom_map=None, undef_code="X"):

    if custom_map is None:
        custom_map = {"Ter": "*"}
    # reverse map of threecode
    # upper() on all keys to enable caps-insensitive input seq handling
    onecode = {k.upper(): v for k, v in protein_letters_3to1_extended.items()}
    # add the given termination codon code and custom maps
    onecode.update((k.upper(), v) for k, v in custom_map.items())
    sequence_list = [sequence[3 * i : 3 * (i + 1)] for i in range(len(sequence) // 3)]
    return "".join(onecode.get(aa.upper(), undef_code) for aa in sequence_list)


def convert_to_three_letter(sequence, custom_map=None, undef_code="Xaa"):
    if custom_map is None:
        custom_map = {"*": "Ter"}
    # not doing .update() on IUPACData dict with custom_map dict
    # to preserve its initial state (may be imported in other modules)
    threecode = dict(
        list(protein_letters_1to3_extended.items()) + list(custom_map.items())
    )
    # We use a default of 'Xaa' for undefined letters
    # Note this will map '-' to 'Xaa' which may be undesirable!
    return "".join(threecode.get(aa, undef_code) for aa in sequence)

def get_coordinates_from_index(pdb_dataframe, atom_index):
    return pdb_dataframe.loc[pdb_dataframe["atom_number"] == atom_index][["x_coord", "y_coord", "z_coord"]].values

def get_hydrogen_bond_distances(pdb_dataframe, residue_start, residue_stop, orientation="Parallel"):
    segments = get_segments(pdb_dataframe)
    residues_to_check = np.arange(residue_start, residue_stop + 1, 2)
    if orientation == "Parallel":
        index = [i for i in range(0, len(segments))]
        segment_start = index[0]
        segment_stop = index[-1]
        hbond_distances = np.zeros((segment_stop - segment_start, len(residues_to_check)))
        for i in range(segment_start, segment_stop):
            for j in residues_to_check:
                HN = get_atom(pdb_dataframe, segments[i + 1], j + 1, "HN")
                CO = get_atom(pdb_dataframe, segments[i], j, "O")
                hbond_distances[
                    i - 1, int(np.where(residues_to_check == j)[0])
                ] = euclidean_distance(HN, CO)
        hbond_distances = pandas.DataFrame(hbond_distances)
        return hbond_distances
    else:
        segmentid_pairs = list(combinations(segments, 2))
        pdb_dataframe_2 = pdb_dataframe[pdb_dataframe["residue_number"].isin(range(residue_start, residue_stop + 1))]
        pdb_dataframe_2 = pdb_dataframe_2[pdb_dataframe_2["atom_name"].isin(["HN", "O"])]
        hbond_distances = pandas.DataFrame(index=segments, columns=segments)
        for segment_pair in segmentid_pairs:
            # HN of first segment to O of second segment
            hn_array = pdb_dataframe_2[
                (pdb_dataframe_2["atom_name"] == "HN")
                & (pdb_dataframe_2["segment_id"] == segment_pair[0])][["x_coord", "y_coord", "z_coord"]]
            co_array = pdb_dataframe_2[(pdb_dataframe_2["atom_name"] == "O") & (pdb_dataframe_2["segment_id"] == segment_pair[1])][["x_coord", "y_coord", "z_coord"]]
            hbond_distances[segment_pair[0]][segment_pair[1]] = pandas.DataFrame(
                cdist(co_array, hn_array, metric="euclidean"),
                index=range(residue_start, residue_stop + 1),
                columns=range(residue_start, residue_stop + 1),
            )
            # O  of first segment to HN of second segment
            hn_array2 = pdb_dataframe_2[
                (pdb_dataframe_2["atom_name"] == "HN")
                & (pdb_dataframe_2["segment_id"] == segment_pair[1])
            ][["x_coord", "y_coord", "z_coord"]]
            co_array2 = pdb_dataframe_2[(pdb_dataframe_2["atom_name"] == "O") & (pdb_dataframe_2["segment_id"] == segment_pair[0])][["x_coord", "y_coord", "z_coord"]]
            hbond_distances[segment_pair[1]][segment_pair[0]] = pandas.DataFrame(
                cdist(co_array2, hn_array2, metric="euclidean"),
                index=range(residue_start, residue_stop + 1),
                columns=range(residue_start, residue_stop + 1),
            )
            # Frames are displayed in order of residues, the horizontal represents the first segment, and the vertical represents the second segment

        return hbond_distances


def style_hbond_dataframe(dataframe):
    def color_red(val):
        if val <= 2.0:
            color = "red"
        else:
            color = "none"
        return "color: %s" % color

    dataframe_ = dataframe.style.applymap(color_red)
    return dataframe_


def get_hbond_distances_from_mathematica(pdb_dataframe, reference_file):
    hbond_array = []
    with open(reference_file, "r") as reference:
        for line in reference:
            search = line.split()
            if len(search) > 0 and search[0] == "bond":
                hbond_array.append(search)
    hbond_array = pandas.DataFrame(hbond_array).iloc[:, 1:3].astype("int32")
    hbond_array = hbond_array + 1
    distance_dataframe = pandas.DataFrame()
    atom_array1 = pdb_dataframe.iloc[pandas.Index(pdb_dataframe['atom_number']).get_indexer(hbond_array.iloc[:, 0])]
    atom_array2 = pdb_dataframe.iloc[pandas.Index(pdb_dataframe['atom_number']).get_indexer(hbond_array.iloc[:, 1])]
    distance_dataframe["Segment 1"] = list(atom_array1["segment_id"])
    distance_dataframe["Segment 2"] = list(atom_array2["segment_id"])
    distance_dataframe["Residue 1"] = list(atom_array1["residue_number"])
    distance_dataframe["Residue 2"] = list(atom_array2["residue_number"])
    distance_array = []
    for index, row in hbond_array.iterrows():
        distance_array.append(
            euclidean_distance(
                get_coordinates_from_index(pdb_dataframe, row[1]),
                get_coordinates_from_index(pdb_dataframe, row[2]),
            )
        )
    distance_dataframe["Distances"] = distance_array
    return distance_dataframe


def find_angle(u, v):
    """
    Calculates the angle (degrees) between two vectors (as 1-d arrays) using
    dot product.
    """

    V1 = u / np.linalg.norm(u)
    V2 = v / np.linalg.norm(v)
    return 180 / np.pi * np.arccos(np.dot(V1, V2))


def calculate_dihedrals(prevCO, currN, currCA, currCO, nextN, cutoff=6.5):
    """
    Calculates phi and psi angles for an individual residue.
    """

    # Set CA coordinates to origin
    A = [prevCO[i] - currCA[i] for i in range(3)]
    B = [currN[i] - currCA[i] for i in range(3)]
    C = [currCO[i] - currCA[i] for i in range(3)]
    D = [nextN[i] - currCA[i] for i in range(3)]

    # Make sure the atoms are close enough
    # if max([dist_sq(x) for x in [A,B,C,D]]) > cutoff:
    #    err = "Atoms too far apart to be bonded!"
    #    raise ValueError(err)

    # Calculate necessary cross products (define vectors normal to planes)
    V1 = np.cross(A, B)
    V2 = np.cross(C, B)
    V3 = np.cross(C, D)

    # Determine scalar angle between normal vectors
    phi = find_angle(V1, V2)
    if np.dot(A, V2) > 0:
        phi = -phi

    psi = find_angle(V2, V3)
    if np.dot(D, V2) < 0:
        psi = -psi

    return phi, psi


def calculate_torsion(pdb_dataframe):
    """
    Calculate the backbone torsion angles for a pdb file.
    """
    pdb = pdb_dataframe.text
    residue_list = []
    N = []
    CO = []
    CA = []

    resid_contents = {}
    current_residue = None
    to_take = ["N  ", "CA ", "C  "]
    for line in pdb:
        if line[0:4] == "ATOM" or (line[0:6] == "HETATM" and line[17:20] == "MSE"):

            if line[13:16] in to_take:

                # First residue
                if current_residue == None:
                    current_residue = line[17:26]

                # If we're switching to a new residue, record the previously
                # recorded one.
                if current_residue != line[17:26]:

                    try:
                        N.append(
                            [
                                float(resid_contents["N  "][30 + 8 * i : 38 + 8 * i])
                                for i in range(3)
                            ]
                        )
                        CO.append(
                            [
                                float(resid_contents["C  "][30 + 8 * i : 38 + 8 * i])
                                for i in range(3)
                            ]
                        )
                        CA.append(
                            [
                                float(resid_contents["CA "][30 + 8 * i : 38 + 8 * i])
                                for i in range(3)
                            ]
                        )
                        residue_list.append(current_residue)

                    except KeyError:
                        err = (
                            "Residue %s has missing atoms: skipping.\n"
                            % current_residue
                        )
                        sys.stderr.write(err)

                    # Reset resid contents dictionary
                    current_residue = line[17:26]
                    resid_contents = {}

                # Now record N, C, and CA entries.  Take only a unique one from
                # each residue to deal with multiple conformations etc.
                if line[13:16] not in resid_contents:
                    resid_contents[line[13:16]] = line
                else:
                    err = "Warning: %s has repeated atoms!\n" % current_residue
                    sys.stderr.write(err)

    # Record the last residue
    try:
        N.append(
            [float(resid_contents["N  "][30 + 8 * i : 38 + 8 * i]) for i in range(3)]
        )
        CO.append(
            [float(resid_contents["C  "][30 + 8 * i : 38 + 8 * i]) for i in range(3)]
        )
        CA.append(
            [float(resid_contents["CA "][30 + 8 * i : 38 + 8 * i]) for i in range(3)]
        )
        residue_list.append(current_residue)

    except KeyError:
        err = "Residue %s has missing atoms: skipping.\n" % current_residue
        sys.stderr.write(err)

    # Calculate phi and psi for each residue.  If the calculation fails, write
    # that to standard error and move on.
    labels = []
    dihedrals = []
    for i in range(1, len(residue_list) - 1):
        try:
            dihedrals.append(
                calculate_dihedrals(CO[i - 1], N[i], CA[i], CO[i], N[i + 1])
            )
            labels.append(residue_list[i])
        except ValueError:
            err = "Dihedral calculation failed for %s\n" % residue_list[i]
            sys.stderr.write(err)
    torsion_angles = pandas.DataFrame(dihedrals, columns=["Phi", "Psi"])
    torsion_angles["resdata"] = labels
    torsion_angles["resdata"] = torsion_angles.resdata.apply(lambda x: "".join([str(i) for i in x]))
    torsion_angles[
        ["Residue Name", "Chain ID", "Residue Number"]] = torsion_angles.resdata.str.split(expand=True)
    torsion_angles.drop("resdata", axis=1, inplace=True)
    torsion_angles["Residue Number"] = pandas.to_numeric(torsion_angles["Residue Number"])
    return torsion_angles


def get_chain_ids(pdb_dataframe):
    return pdb_dataframe.chain_id.unique()

def get_current_directory():
    print(os.getcwd())

def change_directory(path_string_windows_or_unix):
    os.chdir(fix_Dropbox_location(path_string_windows_or_unix))
    
def translate_path(path_string_windows_or_unix):
    #For Mac, the OS is 'posix'.  For PC, the OS is "nt"
    directory_string = path_string_windows_or_unix.encode('unicode-escape').decode()
    if os.name == 'posix':
        directory_string = os.path.normpath(directory_string.replace(r'\\', '/'))
    return(os.path.normpath(directory_string))

def fix_Dropbox_location(path_string):
    if path_string != Dropbox_path:
        p = path_string.replace("\\", "/")
        p = p.replace("Dropbox", "dropbox")
        p = p.replace("DropBox", "dropbox")
        p = p[p.find("dropbox"):]
        p = p[p.find("/"):]
        print(p)
        return(translate_path(Dropbox_path + p))
    else:
        return(path_string)

def list_file_type(filetype, return_aslist=False):
    if ("*" in filetype) is False:
        filetype = "*" + filetype
    if return_aslist is True:
        file_list = [file for file in glob.glob(filetype)]
        return file_list
    for file in glob.glob(filetype):
        print(file)


def list_directory(Path=os.getcwd(), return_aslist=False):
    files = os.listdir(Path)
    if return_aslist is True:
        return files
    else:
        for f in files:
            print(f)


def double_click_button(file_name):
    button = ipywidgets.Button(description=file_name, tooltip='launch ' + file_name)
    display(button)
    def button_eventhandler(obj):
        double_click(file_name)
    button.on_click(button_eventhandler)

def double_click(path_or_file_string):
    if os.name == 'nt':
        os.startfile(file_name)
    elif os.name == 'posix':
        command = path_or_file_string;
        command = command.replace(")", "\)")
        command = command.replace(" ", "\ ")
        command = command.replace("(", "\(")
        command = "open " + command
        os.system(command)

def find_potential_clashes(pdb_dataframe, atom_name_1, atom_name_2, distance_limit):
    pdb_dataframe_2 = pdb_dataframe
    pdb_dataframe_2["atom_name"] = pdb_dataframe_2.atom_name.str.slice(stop=1)
    atom_array_1 = pdb_dataframe_2.loc[pdb_dataframe_2["atom_name"] == atom_name_1][["x_coord", "y_coord", "z_coord"]]
    atom_array_2 = pdb_dataframe_2.loc[pdb_dataframe_2["atom_name"] == atom_name_2][["x_coord", "y_coord", "z_coord"]]
    if atom_name_1 != atom_name_2:
        distances = cdist(atom_array_1, atom_array_2, metric="euclidean")
    elif atom_name_1 == atom_name_2:
        distances = pdist(atom_array_1)
    distances = distances[distances < distance_limit]
    plt.figure(dpi=1200)
    plt.hist(distances)
    plt.xlabel(
        atom_name_1
        + "-"
        + atom_name_2
        + " Distances up to "
        + str(distance_limit)
        + " angstroms"
    )
    histogram = plt.gcf()
    return histogram


# TODO: x axis all equal 0 to 5


def check_all_potential_clashes(pdb_dataframe, save=False, filename=None, format=".png"):
    distances = [2.4, 2.9, 2.9, 2.75, 3.4, 3.22, 3.25, 3.04, 3.07, 3.1]
    for count, clash in enumerate(list(combinations_with_replacement("HCON", 2))):
        figure = find_potential_clashes(pdb_dataframe, clash[0], clash[1], distances[count])
        if save:
            figure.savefig(
                f"{filename} {clash[0]}-{clash[1]} Potential Clashes{format}",
                facecolor="w",
            )
        figure.set_facecolor("white")
        display(figure)
        plt.clf()

#plot 2D XY Scatter Plots
def list_plot(
    data, #Array of XY Datasets
    title="", #Title of Graph
    xlabel="Anant will complain if you don't label your x-axis", #Label of X-Axis
    ylabel="", #Label of Y-Axis
    datalabels=["", "", "", "", "", ""], #Labels for each XY Series
    plotscale=[0, 0, 0, 0], # [plot_x_min, plot_x_max, plot_y_min, plot_y_max]
    xscale=[0, 0, 0], #[x_min, x_max, x_step]
    yscale=[0, 0, 0], #[y_min, y_max, y_step]
    aspect = 'auto', #set aspect ratio (y/x scale)
    markers=["o", "^", "s", "v", "D", "*"], #shape of data  markers (first in array corresponds to first series, second element to second series etc.)
    markersizes=[5, 6, 5, 5, 5, 5], #size of data marker
    colors=["b", "r", "g", "m", "y", "k"], #color of data marker
    fill="none", #fill of data markers
    majorlen=7, #length of major axis ticks
    minorlen=2, #lenght of minor axis ticks
    lineconnect="none", #connect the data points linearly (connect the dots)
    curveFit=False, #approximate a curve fit (5th order polynomial)
    saveSVG=False, #save plot as an SVG file
):

    # strip data array into individual sets and plot them
    for i in range(len(data)):
        plt.plot(
            data[i][:, 0],
            data[i][:, 1],
            marker=markers[i],
            ms=markersizes[i],
            label=datalabels[i],
            fillstyle=fill,
            linestyle=lineconnect,
            color=colors[i],
        )


    plt.title(title, pad = 12)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    axes = plt.gca()
    axes.set_aspect(aspect)

    if plotscale != [0, 0, 0, 0]:
        plt.axis(plotscale)
    plt.minorticks_on()

    if xscale != [0, 0, 0]:
        plt.xticks(np.arange(xscale[0], xscale[1] + xscale[2], step=xscale[2]))
    plt.tick_params(axis="x", which="major", length=majorlen, bottom = True, top = True)
    plt.tick_params(axis="x", which="minor", length=minorlen, bottom = True, top = True)
    if yscale != [0, 0, 0]:
        plt.yticks(np.arange(yscale[0], yscale[1] + yscale[2], step=yscale[2]))
    plt.tick_params(axis="y", which="major", length=majorlen, left = True, right = True)
    plt.tick_params(axis="y", which="minor", length=minorlen, left = True, right = True)

    if curveFit:
        space = np.linspace(start=plt.xticks()[0][0], stop=plt.xticks()[0][-1], num=100)
        for i in range(len(data)):
            eq = np.polyfit(data[i][:, 0], data[i][:, 1], deg=10)
            plt.plot(
                space,
                np.polyval(eq, space),
                label=("fit " + datalabels[i]),
                color=colors[i],
            )

    if saveSVG:
        plt.savefig(title + ".svg")
    plt.legend(loc="best")
    return plt
        
def find_paravastu_function(search_string):
    paravastu_functions = dir(labmodule)
    return [item for item in paravastu_functions if item.find(search_string) > -1]

def get_paravastu_documentation():
    return help(labmodule)

def get_atom_index(pdb_dataframe, segment_id, residue_num, atom_name):
    dataframe = pdb_dataframe.loc[pdb_dataframe["segment_id"] == segment_id]
    dataframe = dataframe.loc[pdb_dataframe["residue_number"] == residue_num]
    dataframe = dataframe.loc[pdb_dataframe["atom_name"] == atom_name]
    return dataframe.atom_number.values[0]


def get_atom_from_index(pdb_dataframe, atom_index):
    return pdb_dataframe.loc[pdb_dataframe["atom_number"] == atom_index]






